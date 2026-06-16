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
        authorizationGeneration += 1
        let activationGeneration = authorizationGeneration
        
        guard HKHealthStore.isHealthDataAvailable() == true else {
            label.setText("not available")
            startStopButton.setEnabled(false)
            return
        }
        
        guard let quantityType = HKQuantityType.quantityTypeForIdentifier(HKQuantityTypeIdentifierHeartRate) else {
            displayNotAllowed()
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
                    self.displayNotAllowed()
                }
            }
        }
    }

    override func didDeactivate() {
        interfaceActive = false
        authorizationGeneration += 1
        super.didDeactivate()
    }
    
    func displayNotAllowed() {
        label.setText("not allowed")
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
            self.startStopButton.setTitle("Start")
            if let query = self.heartRateQuery {
                self.healthStore.stopQuery(query)
                self.heartRateQuery = nil
            }
            self.workoutSession = nil
            self.label.setText("cannot start")
            NSLog("Workout session failed")
        }
    }
    
    func workoutDidStart(date : NSDate) {
        if let query = createHeartRateStreamingQuery(date) {
            heartRateQuery = query
            healthStore.executeQuery(query)
        } else {
            workoutActive = false
            startStopButton.setTitle("Start")
            if let workout = workoutSession {
                healthStore.endWorkoutSession(workout)
            }
            workoutSession = nil
            label.setText("cannot start")
        }
    }
    
    func workoutDidEnd(date : NSDate) {
        workoutActive = false
        startStopButton.setTitle("Start")
        if let query = heartRateQuery {
            healthStore.stopQuery(query)
            heartRateQuery = nil
        }
        workoutSession = nil
        label.setText("---")
    }
    
    // MARK: - Actions
    @IBAction func startBtnTapped() {
        if (self.workoutActive) {
            //finish the current workout
            self.workoutActive = false
            self.startStopButton.setTitle("Start")
            if let query = self.heartRateQuery {
                self.healthStore.stopQuery(query)
                self.heartRateQuery = nil
            }
            if let workout = self.workoutSession {
                healthStore.endWorkoutSession(workout)
            }
        } else {
            //start a new workout
            self.workoutActive = true
            self.startStopButton.setTitle("Stop")
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
        // adding predicate will not work
        // let predicate = HKQuery.predicateForSamplesWithStartDate(workoutStartDate, endDate: nil, options: HKQueryOptions.None)
        
        guard let quantityType = HKObjectType.quantityTypeForIdentifier(HKQuantityTypeIdentifierHeartRate) else { return nil }
        
        let heartRateQuery = HKAnchoredObjectQuery(type: quantityType, predicate: nil, anchor: anchor, limit: Int(HKObjectQueryNoLimit)) { (query, sampleObjects, deletedObjects, newAnchor, error) -> Void in
            guard self.workoutActive else {return}
            guard self.heartRateQuery === query else {return}
            guard error == nil else {
                self.heartRateQueryDidFail(query)
                return
            }
            guard let newAnchor = newAnchor else {return}
            self.anchor = newAnchor
            self.updateHeartRate(sampleObjects, query: query)
        }
        
        heartRateQuery.updateHandler = {(query, samples, deleteObjects, newAnchor, error) -> Void in
            guard self.workoutActive else {return}
            guard self.heartRateQuery === query else {return}
            guard error == nil else {
                self.heartRateQueryDidFail(query)
                return
            }
            guard let newAnchor = newAnchor else {return}
            self.anchor = newAnchor
            self.updateHeartRate(samples, query: query)
        }
        return heartRateQuery
    }

    func heartRateQueryDidFail(query: HKQuery) {
        dispatch_async(dispatch_get_main_queue()) {
            guard self.workoutActive else {return}
            guard self.heartRateQuery === query else {return}
            self.workoutActive = false
            self.startStopButton.setTitle("Start")
            self.healthStore.stopQuery(query)
            self.heartRateQuery = nil
            if let workout = self.workoutSession {
                self.healthStore.endWorkoutSession(workout)
            }
            self.workoutSession = nil
            self.label.setText("cannot start")
            NSLog("Heart-rate query failed")
        }
    }
    
    func updateHeartRate(samples: [HKSample]?, query: HKQuery) {
        guard let heartRateSamples = samples as? [HKQuantitySample] else {return}
        
        dispatch_async(dispatch_get_main_queue()) {
            guard self.workoutActive else{return}
            guard self.heartRateQuery === query else{return}
            guard let sample = heartRateSamples.last else{return}
            let value = sample.quantity.doubleValueForUnit(self.heartRateUnit)
            guard value >= 0 && value <= 300 else{return}
            self.label.setText(String(UInt16(value)))
            
            // retrieve source from sample
            let name = sample.sourceRevision.source.name
            self.updateDeviceName(name)
            self.animateHeart()
        }
    }
    
    func updateDeviceName(deviceName: String) {
        deviceLabel.setText(deviceName)
    }
    
    func animateHeart() {
        self.animateWithDuration(0.5) {
            self.heart.setWidth(60)
            self.heart.setHeight(90)
        }
        
        let when = dispatch_time(DISPATCH_TIME_NOW, Int64(0.5 * double_t(NSEC_PER_SEC)))
        let queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)
        dispatch_after(when, queue) {
            dispatch_async(dispatch_get_main_queue(), {
                self.animateWithDuration(0.5, animations: {
                    self.heart.setWidth(50)
                    self.heart.setHeight(80)
                })
            })
        }
    }
}
