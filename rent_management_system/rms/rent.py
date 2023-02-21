from models import User,Post
from flask import math
def rent():
 rooms = input("input the no of rooms occupied:")
 
 
 tenants = input("input the names of tenants:")
 
 
 
 rent  = input(  "enter rent payaple per room :")
 ammount = input( )
 x=rent
 y= ammount
 balance=x-y 
 
 balance = int("rent") - int("ammount")
 
 if (balance > 0):
 
     print("you have a balance of " 
           "kindly pay up to finish your rent ")
 
 elif (balance < 0):
       print("you have paid extra"    " rent for this month ")
 elif (balance == 0):
       print("you have cleared rent for this month  ")