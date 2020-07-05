from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse

# stripe start here
import stripe
stripe.api_key = 'sk_test_51GvDgzHHgVlfHoWQCztMqjdhzmLoUa8UJm92wTJn8TfhNn9bIzxyAFZqMLIDY4eIXbZcweZMDhvdMKBzyOLjm42u001alsw2aN'
customer = stripe.Customer.retrieve("cus_HXmZEB5k7ZLxhd")

# Render html
def index(request):
    return render(request, 'index.html')

def managePaymentMethods(request):
    
    return render(request, 'manage-payment-methods.html')
    
def charge(request):
    amount = 690 #remember to make this dynamic

    if request.method == 'POST':
        print('Data:', request.POST)
        charge = createCharge(amount)
        # COMMENTED OUT TO TEST CARD PAYMENTS for 1 CUSTOMER
        # customer = stripe.Customer.create(
        #     email=request.POST['email'],
        #     name =request.POST['nickname'],
        #     source = request.POST['stripeToken']
        #     )
        
        
        # card = stripe.Customer.create_source( # CREATE A CARD
        #     customer.id,
        #     source= request.POST['stripeToken'],
        #     )


        # card = stripe.Customer.retrieve_source(
        #     customer.id,
        #     "card_1GyxM5HHgVlfHoWQhVdervbz",
        # )
        
    return redirect(reverse('success', args=[amount]))

def successMsg(request, args):
    amount = args
    return render(request, 'success.html', {'amount':amount})

def checkCustomer(request): #not done, save for later
    #if not yet exist, create new
    customer = stripe.Customer.create(
            email=request.POST['email'],
            name =request.POST['nickname'],
            source = request.POST['stripeToken'],
            )
    # otherwise identify and retrieve
    customerID=None #retrieve customer ID from database
    customer = stripe.Customer.retrieve(customerID)

def saveCard(request):
    card = stripe.Customer.create_source( # CREATE A CARD from input FORM
            customer.id,
            source= request.POST['stripeToken'],
            ) # has this existed yet?

#temporarily used ONLY for testing
def listCard():
    # tags = ["brand", "last4", "funding", "exp_month", "exp_year", "id"]
    for card_data in customer.sources.data:
        temp = [card_data.brand, card_data.last4, card_data.funding, card_data.exp_month, card_data.exp_year, card_data.id]
        print(temp)

# Delete source (card) from a Customer, given which card it is
def deleteCard(card_index):
    '''
    card_index: int
    '''
    card_data = customer.sources.data[0] # Default card's data
    
    del_card = stripe.Customer.delete_source( # delete Default card
        customer.id,
        card_data.id,
    )
    # Might want to prevent customers on paid subscriptions from deleting all cards on file, 
    # so that there is at least one default card for the next invoice payment attempt.
    return del_card

def createCharge(amount):
    return stripe.Charge.create( # CREATE A CHARGE for Customer with DEFAULT card
            customer = customer.id,
            amount = amount, 
            currency = 'usd',
            description = 'example charge',
            )
