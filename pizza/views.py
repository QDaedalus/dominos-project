from django.shortcuts import render
from .forms import PizzaForm, MutiplePizzaForm
from django.forms import formset_factory
from .models import Pizza
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'pizza/home.html')


def login(request):
    return render(request, 'pizza/login.html')

def register(request):
    return render(request, 'pizza/register.html')



def order(request):
    multiple_form = MutiplePizzaForm()
    #order verildikten sonra bize dondurulen sayfadir
    if request.method == 'POST':
        # request.FILES formun dosya kaydetmesine izin verir
        filled_form = PizzaForm(request.POST, request.FILES)
        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            note = 'Thanks for ordering! Your %s %s %s pizza on its way'\
                   % (filled_form.cleaned_data['size'],
                     filled_form.cleaned_data['topping1'],
                     filled_form.cleaned_data['topping2'],)
            new_form = PizzaForm()
            print('helal olsun guzel order'+str((filled_form.cleaned_data['size'])))
            return render(request, 'pizza/order.html', {'created_pizza_pk':created_pizza_pk, 'pizzaform': new_form, 'note': note, 'multiple_form': multiple_form})
    else:
        #order verilmeden dondurulen sayfa
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaform': form ,'multiple_form': multiple_form})
def pizzas(request):
    print('anan')
    number_of_pizzas = 2
    filled_multiple_pizza_form = MutiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():

            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note = 'Pizzas have been ordered!'
        else:
            note = 'Order is not created try again'
        return render(request, 'pizza/pizzas.html', {'note': note, 'formset':formset
                                                     })
    else:
        return render(request, 'pizza/pizzas.html', {'formset':formset})


def edit_order(request, pk):

    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = 'Order updated.'
            context = {'pizzaform': form, 'pizza': pizza, 'note': note}
            return render(request, 'pizza/edit_order.html', context)
    context = {'pizzaform':form, 'pizza':pizza}
    return render(request, 'pizza/edit_order.html', context)
