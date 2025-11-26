from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InputTaskSerializer
from .scoring import analyze_tasks, CircularDependencyError

# module-level store for last analyzed results (non-persistent)
_last_analyzed = None

class AnalyzeTasksAPIView(APIView):
    """
    POST /api/tasks/analyze/
    Accepts JSON array of tasks. Returns sorted tasks with 'score' and 'explanation'.
    Optional query param: ?strategy=fastest_wins|high_impact|deadline_driven|smart_balance
    """
    def post(self, request):
        payload = request.data
        if not isinstance(payload, list):
            return Response({"detail":"Expected a JSON array of tasks."}, status=status.HTTP_400_BAD_REQUEST)

        validated = []
        for obj in payload:
            ser = InputTaskSerializer(data=obj)
            if not ser.is_valid():
                return Response({"detail":"Invalid task data", "errors": ser.errors, "task": obj}, status=status.HTTP_400_BAD_REQUEST)
            validated.append(ser.validated_data)

        strategy = request.query_params.get('strategy', 'smart_balance')
        try:
            scored = analyze_tasks(validated, strategy=strategy)
        except CircularDependencyError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail":"Analysis failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        global _last_analyzed
        _last_analyzed = scored

        return Response({"tasks": scored}, status=status.HTTP_200_OK)

class SuggestTasksAPIView(APIView):
    """
    GET /api/tasks/suggest/
    Returns top 3 tasks from last analysis with a short explanation why.
    """
    def get(self, request):
        global _last_analyzed
        if not _last_analyzed:
            return Response({"detail":"No analysis available. POST to /api/tasks/analyze/ first."}, status=status.HTTP_400_BAD_REQUEST)
        top3 = _last_analyzed[:3]
        suggestions = []
        for t in top3:
            suggestions.append({
                "id": t.get('id'),
                "title": t.get('title'),
                "score": t.get('score'),
                "why": f"Score components: {t.get('explanation')}"
            })
        return Response({"suggestions": suggestions}, status=status.HTTP_200_OK)
