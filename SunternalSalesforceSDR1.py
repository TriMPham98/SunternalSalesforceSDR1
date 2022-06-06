from numpy import void
import pyautogui
import time
import math

def main():
    # Move mouse to upper left corner to manually end program
    pyautogui.FAILSAFE 

    # Start call cadence timer
    start = time.time()

    # Instantiate Call Disposition Counters
    outBoundCalls = noAnswers = callBack = notInterested = dnq = disconnectedNumber = wrongNumber = hungUp = dnc = newAppointment = 0

    print('\nCommence Operation "Look Ma, No Hands"\n')
    openSalesforce()
    clickSalesforceLogo()

    cadenceContinue = True
    while cadenceContinue:

        print("------------------------------------------------------------\n")
        print("Homeowners called: " + str(outBoundCalls) + "\n")
        print("< Waiting for input: Start Calling >\n")
        callCadence = pyautogui.confirm(title="Start Calling?", buttons=['Yes', 'No'])

        if callCadence == "Yes":
            clickSalesforceLogo()
            closeMostRecentHomeownerTab()
            startCalling()
            closeDropDownNotification()
            viewDetails()
            outBoundCalls += 1

            callContinue = True
            while callContinue:

                print('< Waiting for input: Call End >\n')
                callEnd = pyautogui.confirm(title="End Call?", buttons=['Yes'])
                clickSalesforceLogo()

                if callEnd == "Yes":
                    callContinue = False
                    endCall()
            
            print('< Waiting for input: Disposition Type >\n')
            userInput =  pyautogui.confirm(title='Disposition Type', buttons=['No Answer', 'Call Back', 'Not Interested', 'Hung Up', 'DNQ', 'Disconnected Number', 'Wrong Number', 'DNC', 'New Appointment'])
            clickSalesforceLogo()
            setTelemarketingCallPurpose()

            if userInput == "No Answer":
                setNoAnswerDisposition()
                noAnswers += 1

            elif userInput == "Call Back":
                setCallBackDisposition()
                markComplete()
                callBack += 1
                
            elif userInput == "Not Interested":
                topBarChangePRtoNotInterested()
                setNotInterestedDisposition()
                markComplete()
                notInterested += 1

            elif userInput == "Hung Up":
                topBarChangePRtoNotInterested()
                setHungUpDisposition()
                markComplete()
                hungUp += 1

            elif userInput == "DNQ":
                dnqInput = pyautogui.confirm(buttons=['Has Solar', 'Not Homeowner', 'Low Bill', 'Out of Area'])
                print('< Waiting for input: DNQ Type >\n')
                clickSalesforceLogo()
                topBarChangePRtoDNQ()
                clickDispositionMenu()

                if dnqInput == "Has Solar":
                    dnqHasSolar()
                    print("Setting -DNQ - Has Solar- for Call Disposition\n")
                    pyautogui.moveTo(1760, 790)
                    pyautogui.leftClick()

                elif dnqInput == "Not Homeowner":
                    dnqNotHomeowner()
                    print("Setting -DNQ - Not Homeowner- for Call Disposition\n")
                    pyautogui.moveTo(1760, 861)
                    pyautogui.leftClick()

                elif dnqInput == "Low Bill":
                    dnqLowBill()
                    print("Setting -DNQ - Low Bill- for Call Disposition\n")
                    pyautogui.moveTo(1760, 824)
                    pyautogui.leftClick()

                elif dnqInput == "Out of Area":
                    dnqOutOfArea()
                    print("Setting -DNQ - Out of Area- for Call Disposition\n")
                    pyautogui.moveTo(1760, 904)
                    pyautogui.leftClick()

                markComplete()
                dnq += 1

            elif userInput == "Disconnected Number":
                topBarChangePRtoDNQ()
                dnqBadNumber()
                setDisconnectedNumberDisposition()
                markComplete()
                disconnectedNumber += 1

            elif userInput == "Wrong Number":
                topBarChangePRtoDNQ()
                dnqWrongNumber()
                setWrongNumberDisposition()
                markComplete()
                wrongNumber += 1

            elif userInput == 'DNC':
                topBarChangePRtoDNQ()
                dnqDNC()
                setDNCDisposition()
                markComplete()
                dnc += 1

            elif userInput == 'New Appointment':
                setNewAppointmentDisposition()
                newAppointment += 1

            saveDispositionBox()

        elif callCadence == "No":
            # Stop the cadenceContinue while loop
            cadenceContinue = False
            print("Call Cadence Has Ended\n")

            # End call cadence timer
            end = time.time()
            totalSeconds = end - start
            currentSecond = totalSeconds % 60
            currentMinute = (totalSeconds / 60) % 60
            currentHour = (totalSeconds / 60 / 60) % 24

    printCallSummary()

'''
Open Salesforce
'''
def openSalesforce():
    print("Opening Salesforce on Google Chrome\n")
    pyautogui.moveTo(1000, 600)
    pyautogui.click()
    pyautogui.hotkey('command', 'space')
    pyautogui.write('Google Chrome')
    pyautogui.press('enter')
    pyautogui.hotkey('command', 'l')
    time.sleep(1)
    pyautogui.write('https://baysunsolar123456.lightning.force.com/lightning/page/home')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(4)
    for i in range(3):
        pyautogui.leftClick(pyautogui.locateCenterOnScreen('openWorkQueue.png', confidence=0.9))
    time.sleep(4)

'''
Call Commence Combination
'''

def clickSalesforceLogo():
    pyautogui.leftClick(pyautogui.locateCenterOnScreen('SalesforceLogo.png', confidence=0.9))

def closeMostRecentHomeownerTab():
    print("Closing Most Recent Homeowner Tab\n")
    pyautogui.leftClick(pyautogui.locateCenterOnScreen('closeTab.png', confidence=0.9))

def startCalling():
    print("Starting Next Call\n")
    pyautogui.scroll(1000) # Scroll up to reset
    pyautogui.leftClick(pyautogui.locateCenterOnScreen('startCallingDark.png', confidence=0.9)) # Default Start Calling
    # pyautogui.leftClick(pyautogui.locateCenterOnScreen('callPopup.png', confidence=0.9)) # Popup Start Calling

def closeDropDownNotification():
    print('Clearing Drop Down Notification\n')
    pyautogui.leftClick(pyautogui.locateCenterOnScreen('duplicateX.png', confidence=0.9))

def viewDetails():
    time.sleep(1) 
    print("Viewing Details\n")
    for i in range(3):
        pyautogui.leftClick(pyautogui.locateCenterOnScreen('detailsDark.png', confidence=0.9))
    pyautogui.moveRel(0, 350, duration=0.25)  # Move cursor from details to scroll 
    pyautogui.scroll(-500)  # Scroll to System Size, Price, and Notes

def endCall():
    print("Ending Call\n")
    pyautogui.moveTo(pyautogui.locateCenterOnScreen('phoneDialer.png', confidence=0.9))
    pyautogui.scroll(-150)
    time.sleep(0.25)
    pyautogui.leftClick(pyautogui.locateCenterOnScreen('endCallDark.png', confidence=0.9))

'''
Call Purpose
'''

def setTelemarketingCallPurpose():
    print("Setting -Telemarketing- for Call Purpose\n")

    # Robust
    # pyautogui.leftClick(pyautogui.locateCenterOnScreen('callPurpose.png', confidence=0.9))
    # pyautogui.leftClick(pyautogui.locateCenterOnScreen('telemarketing.png', confidence=0.9))

    # Rapid
    # time.sleep(1) # Compensate for Salesforce Lag
    pyautogui.moveTo(1545, 879)
    pyautogui.leftClick()
    pyautogui.moveTo(1545, 684, duration=0)  # Move to Telemarketing Button
    pyautogui.leftClick()

'''
Call Disposition
'''

def clickDispositionMenu():
    # Robust
    # pyautogui.leftClick(pyautogui.locateCenterOnScreen('callDisposition.png', confidence=0.9))

    # Rapid
    pyautogui.moveTo(1777, 876, duration=0)
    pyautogui.leftClick()
    # time.sleep(2) # Compensate for Salesforce Lag

def setNoAnswerDisposition():
    print("Setting -No Answer- for Call Disposition\n")
    clickDispositionMenu()
    pyautogui.scroll(-200)

    # Robust
    # pyautogui.leftClick(pyautogui.locateCenterOnScreen('noAnswer.png', confidence=0.9))

    #Rapid
    pyautogui.moveTo(1800, 707, duration=0) # Move to No Answer
    pyautogui.leftClick()

def setCallBackDisposition():
    print("Setting -Call Back- for Call Disposition\n")
    clickDispositionMenu()
    pyautogui.moveTo(1764, 675, duration=0) # Move to Call Back
    pyautogui.leftClick()

def setNotInterestedDisposition():
    print("Setting -Not Interested- for Call Disposition\n")
    clickDispositionMenu()
    pyautogui.scroll(-200)
    pyautogui.moveTo(1760, 747, duration=0) # Move to Not Interested
    pyautogui.leftClick()
    time.sleep(1.5)

def setHungUpDisposition():
    print("Setting -Hung Up- as Call Disposition\n")
    clickDispositionMenu()
    pyautogui.scroll(-200)
    pyautogui.moveTo(1755, 633, duration=0) # Move to Hung Up
    pyautogui.leftClick()
    time.sleep(1.5)

def setDisconnectedNumberDisposition():
    print("Setting -Disconnected Number- for Call Disposition\n")
    clickDispositionMenu()
    pyautogui.moveTo(1780, 710, duration=0) # Move to Disconnected Number
    pyautogui.leftClick()
    time.sleep(1.5)

def setWrongNumberDisposition():
    print("Setting -Wrong Number- as Call Disposition\n")
    clickDispositionMenu()
    pyautogui.scroll(-200)
    pyautogui.moveTo(1772, 900, duration=0) # Move to Not Interested
    pyautogui.leftClick()
    time.sleep(1.5)

def setDNCDisposition():
    print("Setting -DNC- as Call Disposition\n")
    clickDispositionMenu()
    pyautogui.scroll(-6)
    pyautogui.moveTo(1755, 739, duration=0) # Move to DNC
    pyautogui.leftClick()

def setNewAppointmentDisposition():
    print("Setting -New Appointment- as Call Disposition\n")
    clickDispositionMenu()
    pyautogui.scroll(-200)
    pyautogui.moveTo(1790, 671, duration=0) # Move to New Appointment
    pyautogui.leftClick()


'''
New Call/Appointment
'''

def setNewCallBack(): 
    pyautogui.press('left') # Improve with more robust implementation
    pyautogui.press('left')
    pyautogui.leftClick(pyautogui.locateCenterOnScreen('newCallBack.png', confidence=0.9))

def setNewAppointment():
    void

'''
Top Bar Status Change
'''

def topBarChangePRtoNotInterested():
    print("Top Bar Change: Pending Reschedule to Not Interested\n")
    pyautogui.moveTo(1200, 775, duration=0)  # Scroll up to middle tab to reset
    pyautogui.scroll(1000)
    pyautogui.moveTo(1457, 264, duration=0) # Left click arrow twice
    pyautogui.leftClick()
    pyautogui.leftClick()
    pyautogui.moveTo(1038, 264, duration=0.5)  # Change status to Not Interested
    pyautogui.leftClick()
    pyautogui.moveTo(1381, 323)  # Mark as Current Status
    pyautogui.leftClick()
    time.sleep(1)

def topBarChangePRtoDNQ():
    print("Top Bar Change: Pending Reschedule to DNQ\n")
    pyautogui.moveTo(1200, 775, duration=0)  # Scroll up to middle tab to reset
    pyautogui.scroll(1000)
    pyautogui.moveTo(1457, 264, duration=0) # Left click arrow twice
    pyautogui.leftClick()
    pyautogui.leftClick()
    pyautogui.moveTo(949, 264, duration=0.5)  # Change status to DNQ
    pyautogui.leftClick()
    pyautogui.moveTo(1381, 323)  # Mark as Current Status
    pyautogui.leftClick()
    time.sleep(2)

'''
DNQ Status Detail
'''

def dnqBadNumber():
    pyautogui.moveTo(769, 448) # Move to Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(754, 683) # Choose -Bad Number- as Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(1296, 889) # Move to Done Button
    pyautogui.leftClick()
    time.sleep(1)

def dnqWrongNumber():
    pyautogui.moveTo(769, 448) # Move to Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(701, 653) # Choose -Wrong Number- as Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(1296, 889) # Move to Done Button
    pyautogui.leftClick()
    time.sleep(1)

def dnqDNC():
    pyautogui.moveTo(769, 448) # Move to Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(646, 521) # Choose -DNC- as Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(1296, 889) # Move to Done Button
    pyautogui.leftClick()
    time.sleep(1)

def dnqHasSolar():
    pyautogui.moveTo(769, 448) # Move to Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(675, 772) # Choose -Has Solar- as Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(1296, 889) # Move to Done Button
    pyautogui.leftClick()
    time.sleep(3)

def dnqNotHomeowner():
    pyautogui.moveTo(769, 448) # Move to Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(665, 602) # Choose -Not Homeowner- as Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(1296, 889) # Move to Done Button
    pyautogui.leftClick()
    time.sleep(3)

def dnqLowBill():
    pyautogui.moveTo(769, 448) # Move to Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(673, 562) # Choose -Low Bill- as Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(1296, 889) # Move to Done Button
    pyautogui.leftClick()
    time.sleep(3)

def dnqOutOfArea():
    pyautogui.moveTo(769, 448) # Move to Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(696, 843) # Choose -Out of Area- as Status Detail
    pyautogui.leftClick()
    pyautogui.moveTo(1296, 889) # Move to Done Button
    pyautogui.leftClick()
    time.sleep(3)

'''
Call Complete Combination
'''
def saveDispositionBox():
    print("Saving and exiting Disposition Popup\n")

    # Robust 
    # pyautogui.leftClick(pyautogui.locateCenterOnScreen('dispositionSave.png', confidence=0.9))

    # Rapid
    pyautogui.moveTo(1850, 1015, duration=0)  # Move to Save Button
    pyautogui.leftClick()

def markComplete():
    print("Marking Complete\n")
    pyautogui.moveTo(687, 600) # Move to middle tab
    pyautogui.scroll(-500)
    pyautogui.moveTo(785, 780) # Move to drop down Custom Step
    pyautogui.leftClick()
    pyautogui.leftClick(pyautogui.locateCenterOnScreen('markComplete.png', confidence=0.9))

def printCallSummary():
    print('You called ' + str(outBoundCalls) + ' homeowners in ' 
        + str(math.trunc(currentHour)) + ' hours, ' 
        + str(math.trunc(currentMinute)) + ' minutes, and ' 
        + str(round(currentSecond, 1)) + ' seconds this session.\n')

    print(str(noAnswers) + ' No Answers\n'
        + str(callBack) + ' Call Backs\n'
        + str(notInterested) + ' Not Interested\'s\n'
        + str(hungUp) + ' Hung Ups\n'
        + str(dnq) + ' DNQ\'s\n'
        + str(disconnectedNumber) + ' Disconnected Numbers\n'
        + str(wrongNumber) + ' Wrong Numbers\n'
        + str(dnc) + ' DNC\'s\n'
        + str(newAppointment) + ' New Appointments\n')

if __name__ == "__main__":
    main()
'''
- Use pyautogui.locateCenterOnScreen() for each button to make code compatible with more devices
    - Mac
        - Monitors
        - Laptops
    - Windows

- Export to a .txt file to track my own stats

- Expand functionality to Pitch Misses

- Expand functionality to Confirmation Calls

- Use Voice Recognition for No Answer Auto Disposition
    - "Please leave your message for..."
    - "Hello. Please leave a message after the tone..."
    - "Hello. No one is available to take your call. Please leave a message after the tone."
    - "Your call has been forwarded to an automated voice message system."
    - "Your call has been forwarded to an automated voice messaging system."
    - "At the tone, please record your message."
    - "I'm sorry, but the person you called..."

'''
