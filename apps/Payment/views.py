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
    try:
        customer = stripe.Customer.retrieve(customerID)
    except Exception:
        print("you suck")
    #if not yet exist, create new
    customer = stripe.Customer.create(
            email=request.POST['email'],
            name =request.POST['nickname'],
            source = request.POST['stripeToken'],
            )
    # otherwise identify and retrieve
    customerID=None #retrieve customer ID from database
    
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

from .models import Customer
def createCustomer(self):
    # Validate username, password, email, and source (tokenID)
    # get stripe_customerID
    customer = stripe.Customer.create(
        email='email@gmail.com',
        name = 'Testiman',
        #check if source = None is possible
        )

    c = Customer(
        username = 'sirTest',
        stripe_customerID = customer.id,
        password = 'password',
        name = 'Testiman',
        email = 'email@gmail.com'
        )

    # do try/catch here
    c.save()

'''
Below is the REST API setup.
This will be used as the BASE to build APIs with Stripe
'''
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomerSerializer
from .models import Customer 

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Card': {
            'List': '/card-list/',              # GET a list of cards of current customer
            'Add Card': '/card-add/',                # POST add/save a new card
            'Delete': '/card-delete/<str:pk>',  # DELETE a card
        },
        'Customer': {
             'List': '/cus-list/',              # GET a list of customers
            'Detail': '/cus-detail/<str:pk>',   # GET a specific customer info
            'Create': '/cus-create/',           # POST create a new customer
            'Update': '/cus-update/<str:pk>',   # POST update a customer info
            'Delete': '/cus-delete/<str:pk>',   # DELETE a customer    
        }
    }

    return Response(api_urls)

# GET a list of customers
@api_view(['GET'])
def customerList(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

# GET a list of customers
@api_view(['GET'])
def customerDetail(request, pk):
    customers = Customer.objects.get(id=pk) 
    serializer = CustomerSerializer(customers, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def customerCreate(request):
    # create a Stripe Customer here
    # retrieve Stripe Customer.id
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['PUT'])
def customerUpdate(request, pk):
    # retrieve the Stripe Customer id here
    # update Customer on stripe
    customers = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(instance=customers, data=request.data)
    if serializer.is_valid():
         serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def customerDelete(request, pk):
    # retrieve the Stripe Customer id here
    # remove Customer from Stripe
    customers = Customer.objects.get(id=pk)
    customers.delete()

    return Response("Item successfully deleted: " + pk)