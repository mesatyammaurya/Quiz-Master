from flask import render_template, request, redirect, session, flash
from models.model import *
from controllers.forms import userRegistrationForm, loginForm
from controllers.appFunctions import getAvgScores

def init_routes(app):

    '''========================================== Home Page ============================================================='''
    @app.route("/")
    def home():

        admin = Admin.query.filter_by(email='admin@littleriddle.com').first()
        if not admin:
            admin = Admin(name='Quiz Master', email='admin@littleriddle.com', password='admin@321')
            db.session.add(admin)
            db.session.commit()
        return render_template("home.html")
    
    
    '''========================================== Register Page ============================================================='''
    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = userRegistrationForm()
        if form.validate_on_submit() and request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            qualification = request.form['qualification']
            dob = request.form['dob']

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already registered.", "danger")
                return render_template('register.html', form=form)

            new_user = User(name=name, email=email, password=password, qualification=qualification, dob=dob)
            db.session.add(new_user)
            db.session.commit()
            session['name'] = name
            session['email'] = email
            session['userType'] = 'user'
            flash('User Registered Successfully', "success")
            return redirect('/dashboard')

        return render_template('register.html', form = form)
    
    
    '''========================================== Login Page ============================================================='''
    @app.route("/login", methods=['GET', 'POST'])
    def login():

        email = session.get('email')
        if email:
            return redirect('/dashboard')
        
        form = loginForm()
        if form.validate_on_submit() and request.method == 'POST':

            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()
            admin = Admin.query.filter_by(email=email).first()

            if user and user.check_password(password):
                session['name'] = user.name
                session['email'] = user.email
                session['userType'] = 'user'
                flash(f'Welcome {user.name}', "success")
                return redirect('/dashboard')
            elif admin and admin.check_password(password):
                session['name'] = admin.name
                session['email'] = admin.email
                session['userType'] = 'admin'
                flash(f'Welcome {admin.name}', "success")
                return redirect('/dashboard')
            else:
                flash("Invalid Username or Password", "danger")
                return render_template('login.html', form= form)

        return render_template("login.html", form= form)
    

    '''========================================== Dashboard ============================================================='''
    @app.route("/dashboard")
    def dashboard():
        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
        key = request.args.get('key')
        search = request.args.get('search')
        # User Dashboard
        if session.get('userType') == 'user':
            user = User.query.filter_by(email=session['email']).first()
            userScores = {score.quizId: score.totalScore for score in user.scores}
            if key == 'subject':
                quizzes = Quiz.query.join(Chapter).join(Subject).filter(Subject.name.ilike(f"%{search}%")).all()
                return render_template('userDashboard.html', user=user, quizzes=quizzes, userScores=userScores)
            elif key == 'chapter':
                quizzes = Quiz.query.join(Chapter).filter(Chapter.name.ilike(f"%{search}%")).all()
                return render_template('userDashboard.html', user=user, quizzes=quizzes, userScores=userScores)
            elif key == 'quizzes':
                quizzes = Quiz.query.filter(Quiz.name.ilike(f"%{search}%")).all()
                return render_template('userDashboard.html', user=user, quizzes=quizzes, userScores=userScores)
            quizzes = Quiz.query.all()
            return render_template('userDashboard.html', user=user, quizzes=quizzes, userScores=userScores)
            
        #admin Dashboard 
        elif session.get('userType') == 'admin':
            admin = Admin.query.filter_by(email=session['email']).first()
            subjects = Subject.query.all()
            userAttempts = {}  
            avgScores = {}
            for subject in subjects:
                uniqueUsers = set() 
                totalUserScore = 0
                totalAttempts = 0              
                quizzes = Quiz.query.join(Chapter).join(Subject).filter_by(id=subject.id).all()
                for quiz in quizzes:
                    scores = Score.query.filter_by(quizId=quiz.id).all()
                    for score in scores:
                        uniqueUsers.add(score.userId)  
                        totalUserScore += score.totalScore
                        totalAttempts += 1
                userAttempts[subject.name] = len(uniqueUsers) 
                avgScores[subject.name] = (totalUserScore / totalAttempts) if totalAttempts > 0 else 0

            return render_template('adminDashboard.html', admin=admin, userAttempts=dict(userAttempts), avgScores=dict(avgScores))
        else:
            flash("Some error occured! Try again", "warning")
            return redirect('/login')
        
    
    '''========================================== Subjects Page ============================================================='''
    @app.route('/subjects')
    def subjects():

        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
        key = request.args.get('key')
        search = request.args.get('search')
        
        # User Subject Page
        if session.get('userType') == 'user':       
            user = User.query.filter_by(email=session['email']).first()
            if key == 'subject':
                subjects = Subject.query.filter(Subject.name.ilike(f"%{search}%")).all()
                return render_template('userSubjects.html', user=user, subjects=subjects)
            elif key == 'chapter':
                subjects = Subject.query.join(Chapter).filter(Chapter.name.ilike(f"%{search}%")).all()
                return render_template('userSubjects.html', user=user, subjects=subjects)
            subjects =Subject.query.all()
            return render_template('userSubjects.html', user=user, subjects=subjects)
        
        # Admin Subject Page
        elif session.get('userType') == 'admin':
            admin = Admin.query.filter_by(email=session['email']).first()
            if key == 'subject':
                subjects = Subject.query.filter(Subject.name.ilike(f"%{search}%")).all()
                return render_template('adminSubjects.html', admin=admin, subjects=subjects)
            elif key == 'chapter':
                subjects = Subject.query.join(Chapter).filter(Chapter.name.ilike(f"%{search}%")).all()
                return render_template('adminSubjects.html', admin=admin, subjects=subjects)
            subjects =Subject.query.all()
            return render_template('adminSubjects.html', admin=admin, subjects=subjects)
        else:
            flash("Some error occured! Try again", "warning")
            return redirect('/dashboard')
        

    '''========================================== Quizzes Page ============================================================='''
    @app.route('/<int:subjectId>/<int:chapterId>/quizzes')
    def quizzes(subjectId, chapterId):
        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')

        subject = Subject.query.get(subjectId)
        chapter = Chapter.query.get(chapterId)
        key = request.args.get('key')
        search = request.args.get('search', '').strip().lower()

        quizzes = chapter.quizzes  # Get all quizzes for the chapter

        if search:
            if key == "quizzes":
                quizzes = [quiz for quiz in quizzes if search in quiz.name.lower()]
            elif key == "questions":
                quizzes = [quiz for quiz in quizzes if any(search in ques.title.lower() for ques in quiz.questions)]

        if session.get('userType') == 'user':
            user = User.query.filter_by(email=session['email']).first()
            userScores = {score.quizId: score.totalScore for score in user.scores}
            return render_template('userQuizzes.html', user=user, chapter=chapter, subject=subject, userScores=userScores, quizzes=quizzes)
        elif session.get('userType') == 'admin':
            admin = Admin.query.filter_by(email=session['email']).first()
            return render_template('adminQuizzes.html', admin=admin, chapter=chapter, subject=subject, quizzes=quizzes)
        else:
            flash("Some error occurred! Try again", "warning")
            return redirect(f'/{subjectId}/chapters')



    '''========================================== Admin Dashboard - Manage User ============================================================='''
    @app.route('/manageUsers', methods=['GET', 'POST'])
    def manageUsers():
        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
        admin = Admin.query.filter_by(email=session['email']).first()
        avgScores = getAvgScores(db.session)
        key = request.args.get('key')
        search = request.args.get('search')
        if key == 'user':
            users = User.query.filter(User.name.ilike(f"%{search}%")).all()
            return render_template('adminManageUsers.html', users=users, admin=admin, avgScores=avgScores)
        elif key == 'qualification':
            users = User.query.filter(User.qualification.ilike(f"%{search}%")).all()
            return render_template('adminManageUsers.html', users=users, admin=admin, avgScores=avgScores)
        users = User.query.all()
        return render_template('adminManageUsers.html', users=users, admin=admin, avgScores=avgScores)
    
    
    '''========================================== Admin Dashboard - Delete User ============================================================='''
    @app.route('/deleteUser', methods=['GET', 'POST'])
    def deleteUser():
        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
        id = request.form['id']
        user = User.query.filter_by(id=id).first()
        try:
            db.session.delete(user)
            db.session.commit()
            flash(f'User ({user.name}) deleted successfully', "success")
            return redirect('/manageUsers')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "warning")
            return redirect('/manageUsers')


    '''========================================== Admin Dashboard - Add Subject ============================================================='''
    @app.route('/addSubject', methods=['GET', 'POST'])
    def addSubject():
        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
        
        name = request.form['name']
        desc = request.form['desc']

        try:
            newSubject = Subject(name=name, desc=desc)
            db.session.add(newSubject)
            db.session.commit()
            flash("Subject added successfully", "success")
            return redirect('/subjects')
        except Exception as e:
            db.session.rollback()
            flash(f"Error:- {str(e)}", "warning")
            return redirect('/subjects')
        

    '''========================================== Admin Dashboard - Edit Subject ============================================================='''
    @app.route('/editSubject', methods=['GET', 'POST'])
    def editSubject():
        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login') 
        
        id = request.form['id'] 
        name = request.form['name']      
        desc = request.form['desc']     
        subject = Subject.query.get(id)

        try:
            subject.name = name  
            subject.desc = desc  
            db.session.commit()  
            flash("Subject updated successfully", "success")
            return redirect('/subjects')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "warning")
            return redirect('/subjects')


    '''========================================== Admin Dashboard - Delete Subject ============================================================='''
    @app.route('/deleteSubject', methods=['GET', 'POST'])
    def deleteSubject():
        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
         
        id = request.form['id']
        subject = Subject.query.get(id)
        try:
            db.session.delete(subject)
            db.session.commit()
            flash("Subject deleted successfully", "success")
            return redirect('/subjects')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "warning")
            return redirect('/subjects')


    '''========================================== Admin Dashboard - Add Chapter ============================================================='''
    @app.route('/addChapter', methods=['GET', 'POST'])
    def addChapter():

        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
        subjectId = request.form['subjectId']
        name = request.form['name']
        desc = request.form['desc']

        try:
            newChapter = Chapter(name=name, desc=desc, subjectId=subjectId)
            db.session.add(newChapter)
            db.session.commit()
            flash("Chapter added successfully", "success")
            return redirect('/subjects')
        except Exception as e:
            db.session.rollback()
            flash(f"Error:- {str(e)}", "warning")
            return redirect('/subjects')
        

    '''========================================== Admin Dashboard - Edit Chapter ============================================================='''
    @app.route('/editChapter', methods=['GET', 'POST'])
    def editChapter():
        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login') 
        
        id = request.form['id'] 
        name = request.form['name']      
        desc = request.form['desc']     
        chapter = Chapter.query.get(id)

        try:
            chapter.name = name  
            chapter.desc = desc  
            db.session.commit()  
            flash("Chapter updated successfully", "success")
            return redirect('/subjects')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "warning")
            return redirect('/subjects')


    '''========================================== Admin Dashboard - Delete Chapter ============================================================='''
    @app.route('/deleteChapter', methods=['GET', 'POST'])
    def deleteChapter():
        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
         
        id = request.form['id']
        chapter = Chapter.query.get(id)
        try:
            db.session.delete(chapter)
            db.session.commit()
            flash("Chapter deleted successfully", "success")
            return redirect('/subjects')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "warning")
            return redirect('/subjects')

    
    '''========================================== Admin Dashboard - Add Quiz ============================================================='''
    @app.route('/<int:subjectId>/<int:chapterId>/addQuiz', methods=['GET', 'POST'])
    def addQuiz(subjectId, chapterId):

        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
        
        name = request.form['name']
        dateStr = request.form['date']
        date = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M")  
        duration = request.form['duration']
        desc = request.form['desc']

        try:
            newQuiz = Quiz(name=name, desc=desc,date=date, duration=int(duration), chapterId=chapterId)
            db.session.add(newQuiz)
            db.session.commit()
            flash("Quiz added successfully", "success")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')
        except Exception as e:
            db.session.rollback()
            flash(f"Error:- {str(e)}", "warning")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')
        

    '''========================================== Admin Dashboard - Edit Quiz ============================================================='''
    @app.route('/<int:subjectId>/<int:chapterId>/editQuiz', methods=['GET', 'POST'])
    def editQuiz(subjectId, chapterId):
        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login') 

        id = request.form['id'] 
        name = request.form['name']
        dateStr = request.form['date']
        date = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M")
        duration = request.form['duration']      
        desc = request.form['desc']     
        quiz = Quiz.query.get(id)

        try:
            quiz.name = name
            quiz.date = date
            quiz.duration = duration
            quiz.desc = desc
            db.session.commit()  
            flash("Quiz updated successfully", "success")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "warning")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')


    '''========================================== Admin Dashboard - Delete Quiz ============================================================='''
    @app.route('/<int:subjectId>/<int:chapterId>/deleteQuiz', methods=['GET', 'POST'])
    def deleteQuiz(subjectId, chapterId):

        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
        
        id = request.form['id']
        quiz = Quiz.query.get(id)
        try:
            db.session.delete(quiz)
            db.session.commit()
            flash("Quiz deleted successfully", "success")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "warning")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')


    '''========================================== Admin Dashboard - Add Question ============================================================='''
    @app.route('/<int:subjectId>/<int:chapterId>/addQuestion', methods=['GET', 'POST'])
    def addQuestion(subjectId, chapterId):

        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
        quizId = request.form['quizId']
        title = request.form['title']
        statement = request.form['statement']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correctOption = request.form['correctOption']

        try:
            newQuestion = Question(title=title, statement=statement, option1=option1, option2=option2, option3=option3, option4=option4, correctOption=correctOption, quizId=quizId)
            db.session.add(newQuestion)
            db.session.commit()
            flash("Question added successfully", "success")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')
        except Exception as e:
            db.session.rollback()
            flash(f"Error:- {str(e)}", "warning")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')
        

    '''========================================== Admin Dashboard - Edit Question ============================================================='''
    @app.route('/<int:subjectId>/<int:chapterId>/editQuestion', methods=['GET', 'POST'])
    def editQuestion(subjectId, chapterId):

        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
        
        id = request.form['id']
        title = request.form['title']
        statement = request.form['statement']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correctOption = request.form['correctOption']
        ques = Question.query.get(id)

        try:
            ques.title = title
            ques.statement = statement
            ques.option1 = option1
            ques.option2 = option2
            ques.option3 = option3
            ques.option4 = option4
            ques.correctOption = correctOption
            db.session.commit()
            flash("Question updated successfully", "success")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')
        except Exception as e:
            db.session.rollback()
            flash(f"Error:- {str(e)}", "warning")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')


    '''========================================== Admin Dashboard - Delete Question ============================================================='''
    @app.route('/<int:subjectId>/<int:chapterId>/deleteQuestion', methods=['GET', 'POST'])
    def deleteQuestion(subjectId, chapterId):

        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')
        
        id = request.form['id']
        question = Question.query.get(id)
        try:
            db.session.delete(question)
            db.session.commit()
            flash("Question deleted successfully", "success")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "warning")
            return redirect(f'/{subjectId}/{chapterId}/quizzes')


    '''========================================== User Dashboard - Quiz Attempt ============================================================='''
    @app.route('/<int:quizId>/quizAttempt', methods=['GET', 'POST'])
    def quizAttempt(quizId):

        email = session.get('email')
        user = User.query.filter_by(email=email).first()
        quiz = Quiz.query.get(quizId)

        if request.method == 'POST':
            totalScore = 0
            for ques in quiz.questions:
                quesId = ques.id
                selectedOption = request.form.get(str(quesId))

                if selectedOption is None:
                    score = 0 
                    selectedOption = 0
                else:
                    selectedOption = int(selectedOption)
                    correctOption = ques.correctOption
                    score = 1 if selectedOption == correctOption else 0
                totalScore += score 
                response = Response.query.filter_by(userId=user.id, quizId=quizId, questionId=quesId).first()

                if response:
                    response.selectedOption = selectedOption
                    response.score = score
                else:
                    new_response = Response(userId=user.id, quizId=quizId, questionId=quesId, selectedOption=selectedOption, score=score)
                    db.session.add(new_response)

            newScore = Score(userId=user.id, quizId=quizId, totalScore=totalScore)
            db.session.add(newScore)
            db.session.commit()

            responses = { response.questionId: response for response in Response.query.filter_by(userId=user.id, quizId=quizId).all()}

            return render_template('userResponse.html', quiz=quiz, totalScore=totalScore, responses=responses)

        return render_template('userQuizAttempt.html', quiz=quiz)


    '''========================================== User Dashboard - Past Attempt ============================================================='''
    @app.route('/pastAttempts', methods=['GET', 'POST'])
    def pastAttempt():

        email = session.get('email')
        user = User.query.filter_by(email=email).first()
        key = request.args.get('key')
        search = request.args.get('search')
        if key == 'subject':
            scores = Score.query.filter_by(userId=user.id).join(Quiz).join(Chapter).join(Subject).filter(Subject.name.ilike(f"%{search}%")).order_by(desc(Score.timestamp)).all()
            return render_template('userPastAttempt.html', scores=scores, user=user)
        elif key == 'chapter':
            scores = Score.query.filter_by(userId=user.id).join(Quiz).join(Chapter).filter(Chapter.name.ilike(f"%{search}%")).order_by(desc(Score.timestamp)).all()
            return render_template('userPastAttempt.html', scores=scores, user=user)
        elif key == 'quizzes':
            scores = Score.query.filter_by(userId=user.id).join(Quiz).filter(Quiz.name.ilike(f"%{search}%")).order_by(desc(Score.timestamp)).all()
            return render_template('userPastAttempt.html', scores=scores, user=user)
        scores = Score.query.filter_by(userId=user.id).order_by(desc(Score.timestamp)).all()
        return render_template('userPastAttempt.html', scores=scores, user=user)
  
  
    '''========================================== User Dashboard - Summary ============================================================='''
    @app.route('/userSummary')
    def userSummary():
        email = session.get('email')
        if not email:
            flash("Session expired. Please log in again.", "warning")
            return redirect('/login')

        user = User.query.filter_by(email=email).first()
        subjects = Subject.query.all()
        quizzesAttempted = {}  
        avgScores = {}  

        for subject in subjects:
            totalUserScore = 0
            totalAttempts = 0

            quizzes = Quiz.query.join(Chapter).join(Subject).filter_by(id=subject.id).all()
            for quiz in quizzes:
                score = Score.query.filter_by(userId=user.id, quizId=quiz.id).first()
                if score:
                    totalUserScore += score.totalScore
                    totalAttempts += 1

            quizzesAttempted[subject.name] = totalAttempts
            avgScores[subject.name] = (totalUserScore / totalAttempts) if totalAttempts > 0 else 0

        return render_template('userSummary.html', user=user, quizzesAttempted=quizzesAttempted, avgScores=avgScores)


    '''============================================================ Logout ================================================================='''
    @app.route('/logout')
    def logout():

        session.pop('email', None)
        session.pop('name', None)
        session.pop('userType', None)
        flash("Logged Out", "danger")
        return redirect('/')
    

    
    
    
    