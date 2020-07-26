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
def __listCard():
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

'''
Below is the REST API setup.
This will be used as the BASE to build APIs with Stripe. No idea what all this really means.
'''
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serializers import CustomerSerializer
from .models import Customer 
 
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Card': {
            'List': '/card-list/',              # GET a list of cards of current card
            'Detail': '/card-list/<str:pk>',   # GET a specific card info
            'Save': '/card-create/',            # POST save a new card
            'Update': '/card-update/<str:pk>',   # POST update a card info
            'Delete': '/card-delete/<str:pk>',  # DELETE a card
        },
        'Customer': {
            'List': '/customers/',               # GET a list of customers
            'Detail': '/customers/<str:pk>',   # GET a specific customer info
            'Create': '/customers/',           # POST create a new customer
            'Update': '/customers/<str:pk>',   # POST update a customer info
            'Delete': '/customers/<str:pk>',   # DELETE a customer    
        }
    }

    return Response(api_urls)

'''
Customer API:
class CustomerList: GET the list of customers || POST create new Customer
class CustomerDetail: GET a customer || PUT update a customer || DELETE a customer
'''

class CustomerList(APIView):
    """
    List all customers, or create a new customer.
    """
    def get(self, request, format=None):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # create a Stripe Customer here
        new_customer = stripe.Customer.create(
            email=request.data['email'],
            name =request.data['name'],
            )

        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['stripe_customerID'] = new_customer.id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetail(APIView):
    """
    Retrieve, update or delete a Customer instance.
    """
    def get_object(self, pk):
        try:
            return Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        customers = self.get_object(pk) #get pk from url
        serializer = CustomerSerializer(customers, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        # retrieve the Stripe Customer id here
        # update Customer on stripe
        customers = self.get_object(pk)

        serializer = CustomerSerializer(customers, data=request.data)
        if serializer.is_valid():
            stripe.Customer.modify(
                customers.stripe_customerID,
                name = request.data['name'],
                email = request.data['email'],
                #some metadata?
                )
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customers = self.get_object(pk)
        # remove Customer from Stripe
        stripe.Customer.delete(customers.stripe_customerID)

        customers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
Cards API (given the Customer object from Stripe API)
_______________NOT_READY____________________________
'''
class CardList(APIView):
    def get_object(self, pk):
        try:
            return Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            raise Http404
    # GET return a list of cards of specific customer from Stripe
    def get(self, request, customer_id, format=None):
        #given 'customer' Stripe object
        customers = self.get_object(customer_id)
        stripe_customer = stripe.Customer.retrieve(
            customers.stripe_customerID,
        )
        # get Cards.data
        return Response(stripe_customer.sources.data)
    
    # POST create a new card and add to Stripe
    def post(self, request, customer_id, format=None):     
        # card verification is done automatically (in most cases) by Stripe upon creation
        new_card = stripe.Customer.create_source(
            self.get_object(customer_id).stripe_customerID,
            source= request.POST['stripeToken'],
        )
        
        return Response(new_card)

class CardDetail(APIView):
    def get_object(self, pk):
        try:
            return Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, customer_id, card_id, format=None):
        # Retrieve specific card
        card = stripe.Customer.retrieve_source(
            self.get_object(customer_id).stripe_customerID,
            card_id,
        )
        return Response(card)

    def delete(self, request, customer_id, card_id, format=None):
        # !CHECK if card_id is valid (exception handling)!

        # retrieve Stripe Card
        card = stripe.Customer.delete_source(
            self.get_object(customer_id).stripe_customerID,
            card_id,
        )
        return Response(card, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, customer_id, card_id, format=None):
        '''
        Try-except Cards API for valid input
        '''
        # retrieve Stripe card.id
        card = stripe.Customer.modify_source(
            self.get_object(customer_id).stripe_customerID,
            card_id,
            name=request.data['name'],
        )
        return Response(card)
        # else return Response(status=status.HTTP_400_BAD_REQUEST)
