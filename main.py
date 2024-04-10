# Importing module 
from flask import Flask
import function



mydb = function.connect_to_database()
function.reset_auto_increment(mydb)
print(function.check_balance(mydb,110346862))
#create_account(mydb,'kevin','bananas', 'kevinballs@gmail.com',1221)
#modify_account(mydb,110346862,'kevinRules','socksOff','kevinRules@gmail.com', 1221,)
#delete_account(mydb,None,2)
#print(check_balance(mydb, None, 2))
#deposit_funds(mydb, 110346862, 20)
#withdraw_funds(mydb, 110346862, 20)
#print(check_balance(mydb,110346862))

function.close_connection(mydb)







