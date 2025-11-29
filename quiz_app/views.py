from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event


def home(request):
    """Home page view"""
    quizzes = Quiz.objects.all()[:3]  # Show latest 3 quizzes
    events = Event.objects.filter(date__gte=timezone.now())[:3]  # Show upcoming 3 events
    
    context = {
        'quizzes': quizzes,
        'events': events,
    }
    return render(request, 'quiz_app/home.html', context)


def quiz_list(request):
    """Display all available quizzes"""
    quizzes = Quiz.objects.all()
    
    context = {
        'quizzes': quizzes,
    }
    return render(request, 'quiz_app/quiz_list.html', context)


def quiz_detail(request, quiz_id):
    """Display quiz details before starting"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions_count = quiz.questions.count()
    
    context = {
        'quiz': quiz,
        'questions_count': questions_count,
    }
    return render(request, 'quiz_app/quiz_detail.html', context)


def quiz_attempt(request, quiz_id):
    """Handle quiz attempt - display questions and answers"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('answers').all()
    
    if request.method == 'POST':
        # Get user name
        user_name = request.POST.get('user_name', 'Anonymous')
        
        if not user_name.strip():
            messages.error(request, 'Please enter your name.')
            return redirect('quiz_attempt', quiz_id=quiz_id)
        
        # Create submission
        submission = UserSubmission.objects.create(
            quiz=quiz,
            user_name=user_name,
            score=0
        )
        
        score = 0
        
        # Process each question
        for question in questions:
            # Get selected answer(s)
            selected_answer_ids = request.POST.getlist(f'question_{question.id}')
            
            if not selected_answer_ids:
                continue
            
            # For each selected answer
            for answer_id in selected_answer_ids:
                try:
                    answer = Answer.objects.get(id=answer_id, question=question)
                    is_correct = answer.is_correct
                    
                    # Create user answer
                    UserAnswer.objects.create(
                        submission=submission,
                        question=question,
                        answer=answer,
                        is_correct=is_correct
                    )
                    
                    # Add to score if correct (only count once per question)
                    if is_correct and not UserAnswer.objects.filter(
                        submission=submission,
                        question=question,
                        is_correct=True
                    ).exclude(answer=answer).exists():
                        score += 1
                        break  # Only count one correct answer per question
                        
                except Answer.DoesNotExist:
                    continue
        
        # Update submission score
        submission.score = score
        submission.save()
        
        messages.success(request, 'Quiz submitted successfully!')
        return redirect('quiz_result', submission_id=submission.id)
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quiz_app/quiz_attempt.html', context)


def quiz_result(request, submission_id):
    """Display quiz results"""
    submission = get_object_or_404(UserSubmission, id=submission_id)
    user_answers = submission.user_answers.select_related('question', 'answer').all()
    
    total_questions = submission.quiz.questions.count()
    percentage = submission.calculate_percentage()
    
    # Group user answers by question
    questions_with_answers = {}
    for user_answer in user_answers:
        if user_answer.question.id not in questions_with_answers:
            questions_with_answers[user_answer.question.id] = {
                'question': user_answer.question,
                'user_answers': [],
                'correct_answers': list(user_answer.question.answers.filter(is_correct=True))
            }
        questions_with_answers[user_answer.question.id]['user_answers'].append(user_answer)
    
    context = {
        'submission': submission,
        'total_questions': total_questions,
        'percentage': percentage,
        'questions_with_answers': questions_with_answers.values(),
    }
    return render(request, 'quiz_app/quiz_result.html', context)


def event_list(request):
    """Display all upcoming events"""
    upcoming_events = Event.objects.filter(date__gte=timezone.now())
    past_events = Event.objects.filter(date__lt=timezone.now())
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'quiz_app/event_list.html', context)