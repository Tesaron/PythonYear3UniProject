import csv
import os
import sys
from pathlib import Path
from queue import Queue

'''
Author : Marcelle Prinsloo 9412295097081

Study the scenario and complete the questions that follow:

ER visit scheduler.
Dr. Lagertha Lothbrok heads a private clinic. Recently, she has acquired an emergency room to expand her
services. She typically receives patients with varying levels of conditions, as such[N1] . She has decided on
a rating system to prioritise patients with more critical conditions. When patients are added to the schedule,
they are given a priority level from 1 to 5 (5 being the highest priority) and patients are seen in order of
priority. A patient file (object) is created upon arrival to record the name, surname, and ID number. The
patient is then added to the schedule and a priority level is assigned to the patient object. The patient is then
consulted when it is his/her turn, and a status is assigned to the patient after consultation. She would like to store patient information and the status in a
text file for review. Dr. Lothbrok wants to use a system to help with the scheduling.

You are tasked with creating a Python application that helps the emergency room schedule patients for
doctor consultations, by implementing a data structure to keep track of incoming patients. You must select an
appropriate data structure to maintain the schedule and ensure that critical patients are catered to first. Your application must have the following:

*A patient class: Stores the patient’s name, surname, and ID number. Includes a method to print the
patient’s information.

*A scheduler class: Used to add patient objects to the schedule, retrieve the next patient, print the list of
patients waiting, save patient consultations to a file (in order of occurrence), and read the patient
consultations file.

*A class that implements your data structure: Used to maintain the data structure used to schedule
patients.

*A main menu: Used for navigating the application. The main menu must display options for all
functionalities of the application and must use a sentinel to keep displaying the menu until the application
is terminated.


'''


'''
TODO:
populate the menu

populate the matrix list with patients [Name,Surname,ID]

add print patient option

Create patient scheduler

    Create a file if not exist

    read from file if exist

Schedule new patient > sorted by serevrity > order added FIFO

save patients scheduler > file 
read patients file > scheduler

show next patient

remove patient from scheduler (prompt if patient is done)

'''
#Patient object
class Patient:
    
    def __init__(self,severity,name,lastname,id,consultation):
        self.Severity = severity
        self.Name = name
        self.Lastname = lastname
        self.ID = id
        self.Consultation = consultation
   
    def Addconsultation(self, consultation):
        self.Consultation = consultation
        return self
    
    def printPatient(self):
        print('Name: {}\nLastname: {}\nID: {}'.format(self.Name,self.Lastname,self.ID))
    
    def printPatientFile(self):
        print('Severity: {}\nName: {}\nLastname: {}\nID: {}\nConsultation: {}'.format(self.Severity,self.Name,self.Lastname,self.ID,self.Consultation))

#Patient Scheduler and data structure 
class PatientList(Patient):
    
    dirname = os.path.dirname(os.path.abspath(__file__))
    patientsWaiting_FileName = os.path.join(dirname, 'patientsWaiting.csv')
    consultationsHistory_FileName = os.path.join(dirname, 'consultationsHistory.csv')
    PatientConsultations_FileName = os.path.join(dirname, 'PatientConsultations.csv')
    
    def __init__(self,patientsList=None):
        if patientsList is None:
            self.patientsList = []
        else:
            self.patientsList = patientsList
            
    def addPatient(self,Patient):
        if Patient not in self.patientsList:
            self.patientsList.append(Patient)
            self.SeveritySorter()
            
    def AddPatientConsultation(self,Consultation):
        if(len(self.patientsList)>1):
            patient = self.patientsList[0].Addconsultation (Consultation)
            self.patientsList[0] = patient
            self.printPatientList()
        else:print("No patients on the waiting list")
            
                
    def removePatient(self,Patient):
        if Patient in self.patientsList:
            self.patientsList.remove(Patient)
            
    def popPatient(self):
        self.printConsultedPatients()
        return self.patientsList.pop(0)
        
    def viewPatientsList(self):
        indx = 1
        for p in self.patientsList:
            print(f'Patient [{indx}] : ',p.Name)
            indx +=1
            
    def readPatientList(self):
        path = PatientList.patientsWaiting_FileName  
        my_file = Path(path)
        if my_file.is_file()==True:
                   
            with open (path, 'r') as readfile:
                csv_reader = csv.reader(readfile)    
                for line in csv_reader:
                    temp = list(line)
                    severity = temp[0]
                    name = temp[1]
                    lastname = temp [2]
                    id = temp[3]
                    cons = temp[4]
                    p = Patient(temp[0],temp[1],temp[2],temp[3],temp[4])
                    self.addPatient(p)
    
    def viewPatientsHistory(self):
         path = PatientList.consultationsHistory_FileName
         with open (path, 'r') as readfile:
            csv_reader = csv.reader(readfile)    
            for line in csv_reader:
                temp = list(line)
                p = Patient(temp[0],temp[1],temp[2],temp[3],temp[4])
                print("-----------------------------------------------------------------\n")
                Patient.printPatientFile(p)
            
    #patients waiting
    def printPatientList(self):
        #string builder to ensure file creation is in same directory as the .py file -  Cleaner execution
        path = PatientList.patientsWaiting_FileName
        if(len(self.patientsList)>0):
            my_file = Path(path)
            with open (path, 'w',newline='') as newFile:
                csv_writer = csv.writer(newFile,delimiter=',')
                for p in self.patientsList:
                    tempList = [p.Severity, p.Name,p.Lastname,p.ID,p.Consultation]
                    csv_writer.writerow(tempList)
        else:
            print("No patients in waiting list")
                
    def printConsultedPatients(self):
        #string builder to ensure file creation is in same directory as the .py file -  Cleaner execution
        path = PatientList.consultationsHistory_FileName
        #create file if not exist
        my_file = Path(path)
        if my_file.is_file()==False:
            #create file if not exist
            for p in self.patientsList:
                with open (path, 'w',newline='') as newFile:
                    csv_writer = csv.writer(newFile,delimiter=',')
                    tempList = [p.Severity,p.Name,p.Lastname,p.ID,p.Consultation]
                    csv_writer.writerow(tempList)
        else:
            for p in self.patientsList:
                with open (path, 'a',newline='') as newFile:
                    csv_writer = csv.writer(newFile,delimiter=',')
                    tempList = [p.Severity,p.Name,p.Lastname,p.ID,p.Consultation]
                    csv_writer.writerow(tempList)
            
                
    def getNextPatient(self):
        if(len(self.patientsList)>1):
            CurrPatient = (self.patientsList[0])
            self.popPatient()
            self.printPatientList()
            return(CurrPatient)
        else: print ("No Patients to display")
    

    
    def ViewNextPatient(self):
        if(len(self.patientsList)>1):
         PatientList.printPatientFile(self.patientsList[0]) 
        else: print ("No Patients to display")
    
    def ViewPatientList(self):
        indx = 1
        for Patient in self.patientsList:
            print(f'Patient [{indx}] : ',Patient.Name,' Severity: ',Patient.Severity)
            indx +=1
         
    def printPatientConsultationFile(self):
        #string builder to ensure file creation is in same directory as the .py file -  Cleaner execution
        path = PatientList.PatientConsultations_FileName
        #create file if not exist
        my_file = Path(path)
        if(len(self.patientsList)>1):            
            p = self.patientsList[0]
            with open (path, 'w',newline='') as newFile:
                csv_writer = csv.writer(newFile,delimiter=',')
                severity = ['Case Severity: ',p.Severity]
                name = ['Patient Name: ', p.Name]
                lastname = ['Patient LastName: ', p.Lastname]
                id = ['Patient ID: ', p.ID]
                cons = ['Patient Consultation Notes: ', p.Consultation]
                csv_writer.writerow(name)
                csv_writer.writerow(lastname)
                csv_writer.writerow(id)
                csv_writer.writerow(cons)
                
    
    def SeveritySorter(self):
        temp1 = []
        temp2 = []
        temp3 = []
        temp4 = []
        temp5 = []
        
        for patient in self.patientsList:
            if patient.Severity =='1':
                temp1.append(patient)
                temp1.reverse()
            if patient.Severity =='2':
                temp2.append(patient)
            if patient.Severity =='3':
                temp3.append(patient)
            if patient.Severity =='4':
                temp4.append(patient)
            if patient.Severity =='5':
                temp5.append(patient)
        self.patientsList.clear()
        self.patientsList.extend(temp5)
        self.patientsList.extend(temp4)
        self.patientsList.extend(temp3)
        self.patientsList.extend(temp2)
        self.patientsList.extend(temp1)
    
    def length(self):
        return len(self.patientsList)

    
                

#menu class
sngline = "-----------------------------------------------------------------\n"
dblline = "\n=================================================================\n"    
class Menu():
    PatientList1 = PatientList()
    PatientList1.readPatientList()
    
    def Main():     
        
        print(dblline)
        print("Welcome to the ER Patient Scheduler")
        print(dblline)
        print("Please select one of the following options: ")
        print(sngline)

        print("1.   Enter a new Patient")
        print("2.   Current Patient Options")
        print("3.   View Patient History")
        print("q.   Quit")
        print(sngline)
        
        

        inp = input("Please select your option ->   ")
        
        if(inp == '1'):
            Menu.EnterNewPatient()
            
        
        elif(inp == '2'):
            Menu.currPatientsOpts()
        
        elif(inp == '3'):
            Menu.PatientHistory()
        
        elif (inp == 'q'):
            conf = input ("Are you sure you wish to exit? y/n ->  ")
            if (conf == 'y'):
                Menu.PatientList1.printPatientList()
                sys.exit()
                
            elif (conf =='n'):
                Menu.Main()
            else:
                print("Please choose a valid option\n")
        
        else:
            print("Please choose a valid option\n")


    def EnterNewPatient():
        print(dblline)
        print("Add new Patient Menu")
        print(dblline)
        print("Current Patients Waiting: ")
        Menu.PatientList1.ViewPatientList()
        print(sngline)
        
        while True:
            inp = input ("Do you want to add another Patient? y/n: -> ")
            
            if(inp =='n'):
                Menu.Main()

            elif(inp=='y'):
                severity = input ("Please enter the severity level 1 - 5:   ->")
                name = input ("Please enter Patient Name:   ->")
                lastname = input("Please enter Patient Lastname:   ->")
                id = input("Please enter Patient ID:   ->")
                consultation = 'None'
                newPatient = Patient(severity,name,lastname,id,consultation)
                newPatient.printPatientFile()
                Menu.PatientList1.addPatient(newPatient)
                Menu.PatientList1.ViewPatientList()
            else:print("Please choose a valid option\n")
                



    def currPatientsOpts():
        
        print(dblline)
        print("Current Patient Options")
        print(dblline)
        print("1.   View Next Patient")
        print("2.   Add patient Consultation")
        print("3.   Print Patient File")
        print("4.   Get Next patient")
        print("b.   Back\n")
        
        while True: 
            inp = input("Please select your option ->   ")       
        
            if (inp == '1'):
                print(sngline)
                print('\n')
                Menu.PatientList1.ViewNextPatient()

                print(sngline)
                print("b.   Back to Current Patient Options")
                print("m.   Main menu")

                while True:      
                    inp2 = input("Please select your option ->   ")

                    if(inp2=='b'):
                        Menu.currPatientsOpts()
                        break

                    elif(inp2=='m'):
                        Menu.Main()
                        break
                    else: 
                        print("Please choose a valid option\n")

            elif(inp == '2'):
                print(sngline)
                print('\n')
                Menu.PatientList1.ViewNextPatient()
                if(Menu.PatientList1.length()>1):
                    inp3 = input ("Please enter consultation information for patient:   ->")
                    Menu.PatientList1.AddPatientConsultation(inp3)
                    print ("Changed patient Consultation:")
                    print(sngline)
                    print('\n')
                    Menu.PatientList1.ViewNextPatient()
                    print(sngline)
                    print('\n')
                    while True:
                        inp4 = input("Is the patient done? if yes next patient will be queued y/n:    ->")

                        if(inp4 =='y'):
                            Menu.PatientList1.getNextPatient()
                            Menu.Main()
                            break
                        elif(inp4 =='n'):
                            print("Returning to patient options: ")
                            Menu.currPatientsOpts()
                            break
                        else:print("Please choose a valid option\n")
                else: 
                    print("No Patients in waiting list") 
                    Menu.currPatientsOpts()
                    break
                
            elif(inp == '3'):
                print(sngline)
                print('\n')
                print("Printing current patient information to File: PatientConsultations.csv")
                print('\n')
                Menu.PatientList1.printPatientConsultationFile()
                Menu.currPatientsOpts()
                break

            elif(inp == '4'):
                print(sngline)
                print('\n')
                while True:
                    inp4 = input("Is the patient done? if yes next patient will be queued y/n:    ->")

                    if(inp4 =='y'):
                        Menu.PatientList1.getNextPatient()
                        Menu.Main()
                        break
                    elif(inp4 =='n'):
                        print("Returning to patient options: ")
                        Menu.currPatientsOpts()
                        break
                    else:print("Please choose a valid option\n")

            elif(inp == 'b'):
                print(sngline)
                print('\n')
                Menu.Main()
                break

            else: print("Please choose a valid option\n")
    
    def PatientHistory():
        print(dblline)
        print("Patient History Options")
        print(dblline)
        print("1.   Display Patients")
        print("b.   Back\n")
        
        while True:
            inp = input("Please select your option ->   ")
            
            if (inp =='1'):
                Menu.PatientList1.viewPatientsHistory()
                Menu.Main()
        
        
   
    
#launches the application
menu = Menu()
Menu.Main()




'''patient1 = Patient('1','Test1','Test','Test','Test Consultation')    
patient2 = Patient('2','Test2','Test','Test','Test Consultation')
patient3 = Patient('3','Test3','Test','Test','Test Consultation')
patient4 = Patient('4','Test4','Test','Test','Test Consultation')
patient6 = Patient('5','Test6','Test','Test','Test Consultation')
patient5 = Patient('5','Test5','Test','Test','Test Consultation')


PatientList1 = PatientList()


PatientList1.addPatient(patient1)
PatientList1.addPatient(patient2)
PatientList1.addPatient(patient3)
PatientList1.addPatient(patient4)
PatientList1.addPatient(patient6)
PatientList1.addPatient(patient5)
PatientList1.printPatientList()
#PatientList1.readPatientList()


PatientList1.ViewPatientList()

PatientList1.ViewNextPatient()'''

