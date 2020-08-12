from django.contrib.auth.models import User
from questions.models import Topic, Question


# Getting admin user.
admin = User.objects.get(username="admin")

# Creating help_topic.
help_topic, created = Topic.objects.get_or_create(name="CloudQuestions_Help", creator=admin, color=1)

# What is CloudQuestions?
q1_question = "What is CloudQuestions?"
q1_answer = "<p>CloudQuestions is a personal project that I (Enrique Kessler Martínez) started with the objective of learning the Django framework. CloudQuestions is also my way of creating a better workflow at university, as it helps with the automation of my process. Finally, CloudQuestions is &quot;Efficient learning made easy&quot;, as we combine FlashCards with spaced repetition, helping you reach your full potential.</p>"
q1 = Question.objects.get_or_create(topic=help_topic, question=q1_question, answer=q1_answer)

# How do you add topics?
q2_question = "How do you add topics?"
q2_answer = "<p>You have to be logged in to be able to add topics.</p> <p>There are two ways of adding topics:</p> <ul> <li>File uploading: Files supported are Markdown, which is a common format for text on the web. See below for the format required on questions.</li> <li>Web functionality: Click the &quot;Create topic&quot; button on the questions page. It links to the &quot;Create topic&quot; view, where you can create topics easily.Web functionality: Click the &quot;Create topic&quot; button on the questions page. It links to the &quot;Create topic&quot; view, where you can create topics easily.</li> </ul> <p>Every topic not saved with the &quot;Save&quot; button is discarded.</p>"
q2 = Question.objects.get_or_create(topic=help_topic, question=q2_question, answer=q2_answer)

# What is the format required for questions?
q3_question = "What is the format required for questions?"
q3_answer = "<p>We specify a required format for questions looking for an easier parsing.</p><p>The format is the same as Markdown &quot;Toggles&quot;. These are the following:</p><p>- This is the question.</p><p>&emsp;This is the answer.</p><p>Be aware that the horizontal space on answers must be 4 spaces."
q3 = Question.objects.get_or_create(topic=help_topic, question=q3_question, answer=q3_answer)

# What is the recommended workflow?
q4_question = "What is the recommended workflow?"
q4_answer = """<link href="/static/questions/style.css" rel="stylesheet"><div id="help-topic-container"> <div class="help-topic-section"> <p class="help-topic-title">1. Create a topic</p> <div> <img class="workflow-gif" alt="Creation of topics" src="/static/gifs/workflow-step1.gif"/> </div> </div> <div class="help-topic-section"> <p class="help-topic-title">2. Access the topic</p> <div> <img class="workflow-gif" alt="Creation of topics" src="/static/gifs/workflow-step2.gif"/> </div> </div> <div class="help-topic-section"> <p class="help-topic-title">3. Answer the questions</p> <div> <img class="workflow-gif" alt="Creation of topics" src="/static/gifs/workflow-step3.gif"/> </div> </div> <div class="help-topic-section"> <p class="help-topic-title">4. Rate the topic and revisit</p> <div> <img class="workflow-gif" alt="Creation of topics" src="/static/gifs/workflow-step4.gif"/> </div> </div></div>"""
q4 = Question.objects.get_or_create(topic=help_topic, question=q4_question, answer=q4_answer)

# What is the price for a CloudQuestions' membership?
q5_question = "What is the price for a CloudQuestions' membership?"
q5_answer = """<p>At the moment CloudQuestions is free! You will be able to access all functionality available. If you have any questions feel free to contact us!</p>"""
q5 = Question.objects.get_or_create(topic=help_topic, question=q5_question, answer=q5_answer)

# Which topics am I seeing on the Questions tab?
q6_question = "Which topics am I seeing on the Questions tab?"
q6_answer = """<p>At the current release of CloudQuestions the topics you are seeing in the Questions tab are topics you created. On the browse tab you can check out topics from other users (public topics).</p>"""
q = Question.objects.get_or_create(topic=help_topic, question=q6_question, answer=q6_answer)
