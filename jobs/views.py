# import google.generativeai as genai
# from google import genai
from groq import Groq
import os
from django.db.models import Count
from django.contrib.auth.models import User
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import JobApplication
from .serializers import JobApplicationSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    applications = JobApplication.objects.filter(user=request.user)
    total = applications.count()
    by_status = applications.values('status').annotate(count=Count('status'))
    stats = {'total': total, 'applied': 0, 'interview': 0, 'offer': 0, 'rejected': 0}
    for item in by_status:
        stats[item['status']] = item['count']
    return Response(stats)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def analyze_application(request, pk):
    try:
        application = JobApplication.objects.get(pk=pk, user=request.user)
    except JobApplication.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

    cv_text = request.data.get('cv_text', '')
    job_description = application.job_description

    if not cv_text:
        return Response({'error': 'CV text is required'}, status=status.HTTP_400_BAD_REQUEST)

    if not job_description:
        return Response({'error': 'Job description is missing'}, status=status.HTTP_400_BAD_REQUEST)

    prompt = f"""
    You are a professional HR analyst. Compare this CV against the job description and provide:
    1. A match score from 0 to 100
    2. Key strengths (what matches well)
    3. Key gaps (what is missing)
    4. Specific improvement suggestions

    Job Description:
    {job_description}

    CV:
    {cv_text}

    Respond in this exact format:
    SCORE: [number]
    STRENGTHS: [list strengths]
    GAPS: [list gaps]
    SUGGESTIONS: [list suggestions]
    """



    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    chat = client.chat.completions.create(
     model="llama-3.3-70b-versatile",
     messages=[{"role": "user", "content": prompt}])
    feedback = chat.choices[0].message.content

    score = None
    for line in feedback.split('\n'):
        if line.startswith('SCORE:'):
            try:
                score = int(line.replace('SCORE:', '').strip())
            except:
                pass

    application.ai_feedback = feedback
    application.ai_match_score = score
    application.save()

    return Response({'feedback': feedback, 'match_score': score})