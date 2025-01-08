from django.core.management.base import BaseCommand
from quizzes.models import Category, Quiz, Question
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Add quiz categories and questions'

    def handle(self, *args, **kwargs):
        # Create a default user (admin) for the quizzes
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("No user found. Create a user first."))
            return

        # Define categories and questions
        categories = {
            "Educative": [
                ("What is the capital of France?", "Paris", "London", "Berlin", "Madrid", 1),
                ("What is the chemical symbol for water?", "H2O", "O2", "CO2", "N2", 1),
                ("Who wrote 'Pride and Prejudice'?", "Jane Austen", "Charles Dickens", "Mark Twain", "William Shakespeare", 1),
                # Add more educative questions...
            ],
            "Cultural": [
                ("Which country is known as the Land of the Rising Sun?", "Japan", "China", "South Korea", "India", 1),
                ("What is the traditional dance of Spain?", "Flamenco", "Samba", "Tango", "Polka", 1),
                ("Who painted the Mona Lisa?", "Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Michelangelo", 1),
                # Add more cultural questions...
            ],
            "Fun": [
                ("Which fruit is known for having its seeds on the outside?", "Strawberry", "Banana", "Apple", "Grape", 1),
                ("Which cartoon character lives in a pineapple under the sea?", "SpongeBob SquarePants", "Mickey Mouse", "Bugs Bunny", "Scooby-Doo", 1),
                ("What is the national animal of Scotland?", "Unicorn", "Lion", "Bear", "Eagle", 1),
                # Add more fun questions...
            ],
            "Entertainment": [
                ("Who directed the movie 'Inception'?", "Christopher Nolan", "Steven Spielberg", "James Cameron", "Quentin Tarantino", 1),
                ("Which singer is known as the Queen of Pop?", "Madonna", "Beyoncé", "Lady Gaga", "Ariana Grande", 1),
                ("What is the longest-running TV show?", "The Simpsons", "Friends", "Game of Thrones", "Breaking Bad", 1),
                # Add more entertainment questions...
            ]
        }

        # Create categories and quizzes
        for category_name, questions in categories.items():
            category, created = Category.objects.get_or_create(name=category_name)
            quiz, created = Quiz.objects.get_or_create(
                title=f"{category_name} Quiz",
                description=f"A quiz about {category_name.lower()} topics.",
                category=category,
                created_by=user
            )

            # Add questions to the quiz
            for question_text, option1, option2, option3, option4, correct_option in questions:
                Question.objects.create(
                    quiz=quiz,
                    text=question_text,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    correct_option=correct_option
                )

            self.stdout.write(self.style.SUCCESS(f"Added {len(questions)} questions to the {category_name} category."))

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))

