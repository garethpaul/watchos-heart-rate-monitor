//
//  InterfaceController.swift
//  HeartyMonitor WatchKit Extension
//
//  Created by Gareth on 2/8/16.
//  Copyright © 2016 GarethPaul. All rights reserved.
//

import Foundation
import HealthKit
import WatchKit


class InterfaceController: WKInterfaceController, HKWorkoutSessionDelegate {
    
    @IBOutlet private weak var label: WKInterfaceLabel!
    @IBOutlet private weak var deviceLabel : WKInterfaceLabel!
    @IBOutlet private weak var heart: WKInterfaceImage!
    @IBOutlet private weak var startStopButton : WKInterfaceButton!
    
    let healthStore = HKHealthStore()
    
    //State of the app - is the workout activated
    var workoutActive = false
    var interfaceActive = false
    var authorizationGeneration = 0
    var heartAnimationGeneration = 0
    var statusText = "---"
    var currentDeviceName = ""
    
    // define the activity type and location
    var workoutSession : HKWorkoutSession?
    var heartRateQuery : HKQuery?
    let heartRateUnit = HKUnit(fromString: "count/min")
    var anchor = HKQueryAnchor(fromValue: Int(HKAnchoredObjectQueryNoAnchor))
    
    
    override func awakeWithContext(context: AnyObject?) {
        super.awakeWithContext(context)
    }
    
    override func willActivate() {
        super.willActivate()
        interfaceActive = true
        resetHeartAnimation()
        renderInterfaceState()
        authorizationGeneration += 1
        let activationGeneration = authorizationGeneration

        guard HKHealthStore.isHealthDataAvailable() == true else {
            updateStatusText("not available")
            startStopButton.setEnabled(false)
            return
        }
        
        guard let quantityType = HKQuantityType.quantityTypeForIdentifier(HKQuantityTypeIdentifierHeartRate) else {
            displayAuthorizationFailed()
            return
        }
        
        let dataTypes = Set(arrayLiteral: quantityType)
        startStopButton.setEnabled(false)
        healthStore.requestAuthorizationToShareTypes(nil, readTypes: dataTypes) { (success, error) -> Void in
            dispatch_async(dispatch_get_main_queue()) {
                guard self.interfaceActive &&
                    self.authorizationGeneration == activationGeneration else { return }
                if success == true {
                    self.startStopButton.setEnabled(true)
                } else if success == false {
                    self.displayAuthorizationFailed()
                }
            }
        }
    }

    override func didDeactivate() {
        interfaceActive = false
        authorizationGeneration += 1
        resetHeartAnimation()
        super.didDeactivate()
    }
    
    func displayAuthorizationFailed() {
        updateStatusText("authorization failed")
        startStopButton.setEnabled(false)
    }
    
    func workoutSession(workoutSession: HKWorkoutSession, didChangeToState toState: HKWorkoutSessionState, fromState: HKWorkoutSessionState, date: NSDate) {
        dispatch_async(dispatch_get_main_queue()) {
            guard self.workoutSession === workoutSession else { return }
            switch toState {
            case .Running:
                guard self.workoutActive else { return }
                self.workoutDidStart(date)
            case .Ended:
                self.workoutDidEnd(date)
            default:
                print("Unexpected state \(toState)")
            }
        }
    }
    
    func workoutSession(workoutSession: HKWorkoutSession, didFailWithError error: NSError) {
        dispatch_async(dispatch_get_main_queue()) {
            guard self.workoutSession === workoutSession else { return }
            self.workoutActive = false
            self.resetHeartAnimation()
            self.startStopButton.setTitle("Start")
            if let query = self.heartRateQuery {
                self.healthStore.stopQuery(query)
                self.heartRateQuery = nil
            }
            self.workoutSession = nil
            self.updateDeviceName("")
            self.updateStatusText("cannot start")
            NSLog("Workout session failed")
        }
    }
    
    func workoutDidStart(date : NSDate) {
        anchor = HKQueryAnchor(fromValue: Int(HKAnchoredObjectQueryNoAnchor))
        if let query = createHeartRateStreamingQuery(date) {
            heartRateQuery = query
            healthStore.executeQuery(query)
        } else {
            workoutActive = false
            resetHeartAnimation()
            startStopButton.setTitle("Start")
            if let workout = workoutSession {
                workoutSession = nil
                healthStore.endWorkoutSession(workout)
            }
            updateDeviceName("")
            updateStatusText("cannot start")
        }
    }
    
    func workoutDidEnd(date : NSDate) {
        workoutActive = false
        resetHeartAnimation()
        startStopButton.setTitle("Start")
        if let query = heartRateQuery {
            healthStore.stopQuery(query)
            heartRateQuery = nil
        }
        workoutSession = nil
        updateDeviceName("")
        updateStatusText("---")
    }
    
    // MARK: - Actions
    @IBAction func startBtnTapped() {
        if (self.workoutActive) {
            //finish the current workout
            self.workoutActive = false
            self.resetHeartAnimation()
            self.startStopButton.setTitle("Start")
            self.updateStatusText("---")
            self.updateDeviceName("")
            if let query = self.heartRateQuery {
                self.healthStore.stopQuery(query)
                self.heartRateQuery = nil
            }
            if let workout = self.workoutSession {
                self.workoutSession = nil
                healthStore.endWorkoutSession(workout)
            }
        } else {
            //start a new workout
            self.workoutActive = true
            self.startStopButton.setTitle("Stop")
            self.updateStatusText("---")
            self.updateDeviceName("")
            startWorkout()
        }
        
    }
    
    func startWorkout() {
        let session = HKWorkoutSession(activityType: HKWorkoutActivityType.CrossTraining, locationType: HKWorkoutSessionLocationType.Indoor)
        session.delegate = self
        self.workoutSession = session
        healthStore.startWorkoutSession(session)
    }
    
    func createHeartRateStreamingQuery(workoutStartDate: NSDate) -> HKQuery? {
        guard let quantityType = HKObjectType.quantityTypeForIdentifier(HKQuantityTypeIdentifierHeartRate) else { return nil }
        let predicate = HKQuery.predicateForSamplesWithStartDate(workoutStartDate, endDate: nil, options: HKQueryOptions.StrictStartDate)
        
        let heartRateQuery = HKAnchoredObjectQuery(type: quantityType, predicate: predicate, anchor: anchor, limit: Int(HKObjectQueryNoLimit)) { (query, sampleObjects, deletedObjects, newAnchor, error) -> Void in
            dispatch_async(dispatch_get_main_queue()) {
                self.handleHeartRateQueryResult(query, samples: sampleObjects, newAnchor: newAnchor, error: error)
            }
        }
        
        heartRateQuery.updateHandler = {(query, samples, deleteObjects, newAnchor, error) -> Void in
            dispatch_async(dispatch_get_main_queue()) {
                self.handleHeartRateQueryResult(query, samples: samples, newAnchor: newAnchor, error: error)
            }
        }
        return heartRateQuery
    }

    func handleHeartRateQueryResult(query: HKQuery, samples: [HKSample]?, newAnchor: HKQueryAnchor?, error: NSError?) {
        guard workoutActive else {return}
        guard heartRateQuery === query else {return}
        guard error == nil else {
            heartRateQueryDidFail(query)
            return
        }
        guard let newAnchor = newAnchor else {return}
        anchor = newAnchor
        updateHeartRate(samples, query: query)
    }

    func heartRateQueryDidFail(query: HKQuery) {
        guard self.workoutActive else {return}
        guard self.heartRateQuery === query else {return}
        self.workoutActive = false
        self.resetHeartAnimation()
        self.startStopButton.setTitle("Start")
        self.healthStore.stopQuery(query)
        self.heartRateQuery = nil
        if let workout = self.workoutSession {
            self.workoutSession = nil
            self.healthStore.endWorkoutSession(workout)
        }
        self.updateDeviceName("")
        self.updateStatusText("cannot start")
        NSLog("Heart-rate query failed")
    }
    
    func updateHeartRate(samples: [HKSample]?, query: HKQuery) {
        guard let heartRateSamples = samples as? [HKQuantitySample] else {return}
        
        guard self.workoutActive else{return}
        guard self.heartRateQuery === query else{return}
        guard let sample = heartRateSamples.last else{return}
        let value = sample.quantity.doubleValueForUnit(self.heartRateUnit)
        guard value > 0 && value <= 300 else{return}
        self.updateStatusText(String(UInt16(value)))

        // retrieve source from sample
        let name = sample.sourceRevision.source.name
        self.updateDeviceName(name)
        self.animateHeart()
    }

    func updateStatusText(text: String) {
        statusText = text
        guard interfaceActive else {return}
        label.setText(text)
    }

    func updateDeviceName(deviceName: String) {
        currentDeviceName = deviceName
        guard interfaceActive else {return}
        deviceLabel.setText(deviceName)
    }

    func renderInterfaceState() {
        guard interfaceActive else {return}
        label.setText(statusText)
        deviceLabel.setText(currentDeviceName)
        startStopButton.setTitle(workoutActive ? "Stop" : "Start")
    }
    
    func resetHeartAnimation() {
        heartAnimationGeneration += 1
        heart.setWidth(50)
        heart.setHeight(80)
    }

    func animateHeart() {
        guard interfaceActive else {return}
        guard workoutActive else {return}
        heartAnimationGeneration += 1
        let animationGeneration = heartAnimationGeneration
        self.animateWithDuration(0.5) {
            self.heart.setWidth(60)
            self.heart.setHeight(90)
        }
        
        let when = dispatch_time(DISPATCH_TIME_NOW, Int64(0.5 * double_t(NSEC_PER_SEC)))
        let queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)
        dispatch_after(when, queue) {
            dispatch_async(dispatch_get_main_queue(), {
                guard self.interfaceActive else {return}
                guard self.workoutActive else {return}
                guard self.heartAnimationGeneration == animationGeneration else {return}
                self.animateWithDuration(0.5, animations: {
                    self.heart.setWidth(50)
                    self.heart.setHeight(80)
                })
            })
        }
    }
}
