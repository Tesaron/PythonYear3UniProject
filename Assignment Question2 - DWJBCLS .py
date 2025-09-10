import sys
import matplotlib.pyplot as plotG
import networkx as mynx

'''
Author : Marcelle Prinsloo 9412295097081

Study the scenario and complete the questions that follow:

Social Media Connections Manager
Social media networks use network analysis to discover patterns hidden within the structure of the network.
To do this, graph theory is relied upon. In these networks, individual users are represented by nodes, and the
relationships/connections between these users are represented by edges

Your task is to simulate this analysis by creating a Python application that implements graph theory to
achieve this. Your application must have the following:

*A main menu to select options (the menu must be displayed to the user until the application terminates.
*A connections manager class with the following methods:
    *Add user.
    *Add connection.
    *View all users.
    *View all connections.
    *Display a graph showing all connections in the network.

'''
 
class User:
    
    def __init__(self,name):
        self.Name = name
    
    def printUser(self):
        print(self)

class Connection(User):
    
    UserConnections = []
    Users = []
    
    def __init__(self,connection=None):
        if connection is None:
            self.connectionList = []
        else:
            self.connectionList = self
    def addconn (self,u1,u2):
        tempList = [u1,u2]
        Connection.UserConnections.append(tempList)
        
    def addUser(self,username):
        U1 = username
        if U1 not in Connection.Users:
            Connection.Users.append(U1)
    
    def viewConnections(self):
        for conn in Connection.UserConnections:
            print('{} connected to {}'.format(conn[0],conn[1]))

    def viewUsers(self):
        for user in Connection.Users:
            User.printUser(user)
        
    
        




'''user1 = 'user1'
user2 = 'user2'
user3 = 'user3'
user4 = 'user4'
user5 = 'user5'
 
conn1 = Connection.addconn(user1,user2)
conn2 = Connection.addconn(user2,user3)
conn3 = Connection.addconn(user1,user3)

Connection.addconn(conn1)
Connection.addconn(conn2)
Connection.addconn(conn3)
''' 

sngline = "-----------------------------------------------------------------\n"
dblline = "\n=================================================================\n"   

conn = Connection()

class Menu():
   
    
    def main():
        
        print(dblline)
        print("Welcome to the Social Media Connections Manager")
        print(dblline)
        print("Please select one of the following options: ")
        print(sngline)

        print("1.   Add user")
        print("2.   Add connection")
        print("3.   View all users")
        print("4.   View all connections")
        print("5.   View graph")
        print("q.   Quit")
        print(sngline)
       
        while True:
            
            inp = input("Please select your option ->   ")
            
            if(inp == '1'):
                Menu.AddUser()
                break

            elif(inp == '2'):
                Menu.AddConnection()
                break

            elif(inp == '3'):
                Menu.ViewUsers()
                break

            elif(inp == '4'):
                Menu.ViewConnections()
                break
            
            elif(inp == '5'):
                Menu.DisplayGraph()
                break
            
            elif (inp == 'q'):
                conf = input ("Are you sure you wish to exit? y/n   ->")
                if (conf == 'y'):
                    sys.exit()
            
            else:
                print("Please choose a valid option\n")

    def AddUser():
        print(dblline)
        print("Add User")
        print(dblline)
        print("\n")
        
        while True:
            newuser = input("Please enter User Name:    ->")
            newuser = newuser.lower()
            if(newuser!=''):
                conn.addUser(newuser)
                print('User Added!\n')
            else:
                print('User not Added! Please enter a valid name\n')
            
            prompt = input("Press any key to add another User or press 'n' to go back      ->")
            
            if(prompt=='n'):
                Menu.main()
                break
    
    def AddConnection():
        print(dblline)
        print("Add Connection")
        print(dblline)
        print("\n")
        
        print('User available:\n')
        if(len(conn.Users)==0):
            print('No users available, please add new users first')
            Menu.main()
        else:   
            conn.viewUsers()

        while True:
            user1 = ''
            user2 = ''

            while True:   
                u1 = input('Please enter the name of user1:     ->')
                u1 = u1.lower()
                if u1 not in conn.Users:
                    print('User not in users list, Please enter correct user name\n')
                else:
                    user1 = u1
                    break
                
            while True:   
                u2 = input('Please enter the name of user2:     ->')
                u2 = u2.lower()
                if u1 not in conn.Users:
                    print('User not in users list, Please enter correct user name\n')
                else:
                    user2 = u2
                    break
            if(user1 !='' and user2 !=''):
                conn.addconn(user1,user2)
                
            prompt = input("Press any key to add another connection or press 'n' to go back      ->")
            
            if (prompt == 'n'):
                Menu.main()
                break
    
    def ViewUsers():
        print(dblline)
        print("View Users")
        print(dblline)
        print("\n")
        
        if (len(conn.Users)!=0):
            conn.viewUsers()
            
        input ('Press any key to continue to main menu . . . ')
        Menu.main()
            
        
    def ViewConnections():
        print(dblline)
        print("View Connection")
        print(dblline)
        print("\n")
        
        if (len(conn.UserConnections)!=0):
            conn.viewConnections()
            
        input ('Press any key to continue to main menu . . . ')
        Menu.main()
    
    
    
    def DisplayGraph():
        G = mynx.DiGraph()
        G = mynx.DiGraph()
        G.add_edges_from(conn.UserConnections)
        mylayout = mynx.spring_layout(G)    
        mynx.draw(G,mylayout, with_labels=True, node_color="silver", node_size=1500, font_size=12, font_color='cyan')    
        plotG.title("User Connections")
        plotG.show()
        Menu.main()


m = Menu()
Menu.main()