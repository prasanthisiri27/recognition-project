from django.http import JsonResponse
from recognition.recognition_script import mark_attendance

def start_recognition(request):
    """
    Django view to trigger face recognition and attendance marking.
    """
    try:
        mark_attendance()  # run your recognition logic
        return JsonResponse({"status": "Recognition Finished"})
    except Exception as e:
        return JsonResponse({"status": f"Error: {str(e)}"})
