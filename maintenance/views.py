from django.shortcuts import render, redirect, get_object_or_404
from .models import MaintenanceRequest
from .models import Equipment, Team

def dashboard(request):
    return render(request, "maintenance/home.html")



def request_list(request):
    context = {
        "new": MaintenanceRequest.objects.filter(status="NEW"),
        "in_progress": MaintenanceRequest.objects.filter(status="IN_PROGRESS"),
        "repaired": MaintenanceRequest.objects.filter(status="REPAIRED"),
        "scrap": MaintenanceRequest.objects.filter(status="SCRAP"),
    }
    return render(request, "maintenance/kanban.html", context)


def update_status(request, pk, status):
    req = get_object_or_404(MaintenanceRequest, pk=pk)
    req.status = status
    req.save()
    return redirect("request_list")

def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, "maintenance/equipment_list.html", {
        "equipments": equipments
    })


def equipment_requests(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    requests = equipment.maintenancerequest_set.all()

    return render(request, "maintenance/equipment_requests.html", {
        "equipment": equipment,
        "requests": requests
    })


def create_request(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        equipment_id = request.POST.get("equipment")
        request_type = request.POST.get("request_type")
        scheduled_date = request.POST.get("scheduled_date")

        equipment = Equipment.objects.get(id=equipment_id)

        MaintenanceRequest.objects.create(
            subject=subject,
            equipment=equipment,
            team=equipment.maintenance_team,
            request_type=request_type,
            scheduled_date=scheduled_date
        )

        return redirect("request_list")

    equipments = Equipment.objects.all()

    return render(request, "maintenance/create_request.html", {
        "equipments": equipments
    })

def calendar_view(request):
    from .models import MaintenanceRequest

    requests = MaintenanceRequest.objects.filter(
        request_type="PREVENTIVE"
    ).order_by("scheduled_date")

    grouped = {}

    for r in requests:
        if r.scheduled_date not in grouped:
            grouped[r.scheduled_date] = []
        grouped[r.scheduled_date].append(r)

    return render(request, "maintenance/calendar.html", {
        "grouped": grouped
    })

def create_equipment(request):
    from .models import Equipment, Team

    if request.method == "POST":
        Equipment.objects.create(
            name=request.POST.get("name"),
            serial_number=request.POST.get("serial_number"),
            category=request.POST.get("category"),
            department=request.POST.get("department"),
            location=request.POST.get("location"),
            purchase_date=request.POST.get("purchase_date"),
            warranty_till=request.POST.get("warranty_till"),
            maintenance_team=Team.objects.get(id=request.POST.get("team")),
        )
        return redirect("equipment_list")

    teams = Team.objects.all()
    return render(request, "maintenance/create_equipment.html", {
        "teams": teams
    })

def home(request):
    return render(request, "maintenance/home.html")
