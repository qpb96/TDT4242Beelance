
from django.shortcuts import render, redirect

from projects.models import Project, Task, TaskOffer, PromotedProject, ActivePromotion
from projects.templatetags.project_extras import get_accepted_task_offer
from .forms import PaymentForm
from .models import Payment, PromotionPayment
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required
def payment(request, project_id, task_id):
    sender = Project.objects.get(pk=project_id).user
    task = Task.objects.get(pk=task_id)
    receiver = get_accepted_task_offer(task).offerer

    if request.method == 'POST':
        payment = Payment(payer=sender, receiver=receiver, task=task)
        payment.save()
        task.status = Task.PAYMENT_SENT
        task.save()

        return redirect('receipt', project_id=project_id, task_id=task_id)

    form = PaymentForm()

    return render(request,
                'payment/payment.html', {
                'form': form,
                })

@login_required
def receipt(request, project_id, task_id):

    project = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    taskoffer = get_accepted_task_offer(task)

    return render(request,
                'payment/receipt.html', {
                'project': project,
                'task': task,
                'taskoffer': taskoffer,
                 })

@login_required
def promotion_payment(request, project_id ):
    sender = request.user.profile

    def validate_then_save(model):
        model.clean()
        model.save()
        return model

    if request.method == 'POST':
        try:
            project = Project.objects.get(pk=project_id)
            promoted_project = PromotedProject(project=project)
            promoted_project = validate_then_save(promoted_project)
            active_promotion = ActivePromotion(promoted_project=promoted_project)
            active_promotion = validate_then_save(active_promotion)
            payment = PromotionPayment(payer=sender)
            payment.save()
            messages.success(request, "Payment successful")
            return redirect('project_view', project_id=project_id,)
        except:
            messages.error(request, "Something wrong happend during the transaction.")

    form = PaymentForm()

    return render(request,
                'payment/payment.html', {
                'form': form,
                })