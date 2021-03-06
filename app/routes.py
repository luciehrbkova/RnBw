from flask import render_template, url_for, redirect, flash, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, BoardForm, CardForm, TaskForm, DeleteTaskForm, DeleteCardForm, DoneTaskForm
from flask_login import current_user, login_user
from app.models import User, Board, Card, Task, Quote, Award
from flask_login import logout_user, login_required
from datetime import date, timedelta




@app.route("/")
def index():
    return redirect('/login')

@app.route("/login", methods=['GET', 'POST'])
def login():
    #logged in user tryning to login again - direct him home
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # form validate on submit process the form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('home')
        # return redirect(next_page)
        return redirect(url_for('home'))
        # return redirect(url_for('home'))
        #try flash message
        # flash('Login succsesfull {}'.format(form.email.data))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, name=form.name.data, surname=form.surname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    user = current_user
    recentboards = user.boards.order_by(Board.id.desc()).limit(2).all()
    return render_template('home.html', title='Home', boards=recentboards, user=user)

@app.route("/myboards", methods=['GET', 'POST'])
@login_required
def myboards():
    user = current_user
    boards = user.boards.all()
    # thisboard = board.id
    return render_template('myboards.html', title='My Boards', boards=boards, user=user, greeting="What do you want to work on, today!")

@app.route("/newboard", methods=['GET', 'POST'])
@login_required
def newboard():
    form = BoardForm()
    if form.validate_on_submit():
        board = Board(title=form.title.data, author=current_user)
        db.session.add(board)
        db.session.commit() 
        return redirect(url_for('myboards'))
        # return redirect(url_for('board/board['title']')
    return render_template('board.html', title='New Board', form=form, greeting="Let's start with creating new board!")

@app.route("/board/<boardid>", methods=['GET', 'POST'])
@login_required
def board(boardid):
    user = current_user
    boards = user.boards.all()
    thisboard = Board.query.filter_by(id=boardid).first()
    print (thisboard.title)
    print (thisboard.id)
    thisboardid = thisboard.id
    # display all card on this board________________
    cards = thisboard.cards.order_by(Card.date).all()
    print (cards)
    #display all tasks______________________________
    tasks = Task.query.all()
    # forms__________________________________________
    formCard = CardForm()
    formTask = TaskForm()
    formDeleteTask = DeleteTaskForm()
    formDoneTask = DoneTaskForm()
    formDeleteCard = DeleteCardForm()
   
    # forms___________________________________________
    if request.method =='POST':
        form_name = request.form['form-name']
        if form_name == 'form-newCard':
            if formCard.validate_on_submit():
                cardtaken = Card.query.filter_by(date=formCard.date.data).filter_by(board_id=thisboardid).first()
                if cardtaken is None:
                    card = Card(header=formCard.header.data, date=formCard.date.data, motherboard=thisboard)
                    db.session.add(card)
                    db.session.commit()
        elif form_name == 'form-newTask':
            if formTask.validate_on_submit():
                task = Task(card_id=formTask.card_id.data, tasktext=formTask.tasktext.data)
                db.session.add(task)
                db.session.commit()
                return redirect(url_for('board', boardid=boardid))
        elif form_name == 'form-taskDelete':
            if formDeleteTask.validate_on_submit():
                taskToDelete = Task.query.filter_by(id=formDeleteTask.id.data).first()
                db.session.delete(taskToDelete)
                db.session.commit()
                return redirect(url_for('board', boardid=boardid))
                print(taskToDelete)
        elif form_name == 'form-taskDone':   
            # Done task form
            if formDoneTask.submit3 and formDoneTask.validate():
                taskDone = Task.query.filter_by(id=formDoneTask.id.data).first()
                if taskDone.done == False:
                    taskDone.done = True
                    db.session.commit()
                    return redirect(url_for('board', boardid=boardid))
                elif taskDone.done == True:
                    taskDone.done = False
                    db.session.commit()
                    return redirect(url_for('board', boardid=boardid))
                print(taskDone)
        elif form_name == 'form-cardDelete':   
            # Delete card form
            if formDeleteCard.validate_on_submit():
                if Task.query.filter_by(card_id=formDeleteCard.id.data).first() is None:
                    cardToDelete = Card.query.filter_by(id=formDeleteCard.id.data).first()
                    db.session.delete(cardToDelete)
                    db.session.commit()
                    return redirect(url_for('board', boardid=boardid))
                for task in Task.query.filter_by(card_id=formDeleteCard.id.data).all():
                    #problem with deleting tasks
                    db.session.delete(task)
                    db.session.commit()
                cardToDelete = Card.query.filter_by(id=formDeleteCard.id.data).first()
                db.session.delete(cardToDelete)
                db.session.commit()
                return redirect(url_for('board', boardid=boardid))
   
    # dashboard____________________________________________________________________________
    today = str(date.today())
    allTasksForToday = 0
    doneTasksForToday = 0
    rainbowValue= None
    rainbowMeter = 350
    motivation="Let's do it!"
    import random
    #CARD__________________________
    cardForToday = Card.query.filter_by(date=today).filter_by(board_id=thisboardid).first()
    if cardForToday:
        if cardForToday.completed == False:
            #TODAYS TASKS
            if Task.query.filter_by(card_id=cardForToday.id).first():
                allTasksForToday = Task.query.filter_by(card_id=cardForToday.id).all()
                numberAllTasks = len(allTasksForToday)
                #DONE TODAYS TASKS
                doneTasksForToday = Task.query.filter_by(card_id=cardForToday.id).filter_by(done=True).all()
                numberDoneTasks = len(doneTasksForToday)    
                #RAINBOW VALUE******
                rainbowValue = numberDoneTasks/numberAllTasks
                rainbowMeter = 350-350*rainbowValue
                #MOTIVATION DEPENDENT ON THE TASK SCORE **************
                if numberAllTasks >0 and numberDoneTasks == 0:
                    motivation= "You have " + str(numberAllTasks) + " tasks to complete! Start to achieve your dreams!"
                #1/1
                if numberAllTasks == 1 and numberDoneTasks == 1:
                    motivation="Congratulation! You are simply the best! Everything is done! Enjoy the moment and your free time!"         
                # 2+
                if numberAllTasks > 1:
                    # 1/X
                    if numberDoneTasks == 1:
                        motivation="Congratulation! You have completed your first task! Go ahead!"
                    # 2/X
                    if numberDoneTasks == 2:
                        motivation="Perfect! The second task done! You are on the right track! Don't stop!!!"
                    # 2/2
                    if numberAllTasks == 2 and numberDoneTasks == 2:
                        motivation="Congratulation! You are simply the best! Everything is done! Enjoy the moment and your free time!"
                    # 2+3/3
                    if numberAllTasks == 3:
                        # 2/3
                        if numberDoneTasks == 2:
                            motivation="Hey! You are doing sooo well! only last task to do! Well done! Go Go Go!"
                        # 3/3
                        if numberDoneTasks == 3:
                            motivation="Congratulation! You are simply the best! Everything is done! Enjoy the moment and your free time!"
                    # odd values and < 50%
                    if 0.3 < rainbowValue < 0.41 and numberAllTasks % 2 !=0:
                        motivation="Great job, You! You are beating this game!"
                    if 0.4 < rainbowValue < 0.5 and numberAllTasks % 2 !=0:
                        motivation="You are doing soooo well! Complete one more task are you are in the midway!"
                    # even values and < 50%
                    if 0.2 < rainbowValue < 0.31 and numberAllTasks % 2 == 0:
                        motivation="Great job, You! You are beating this game!"
                    if 0.3 < rainbowValue < 0.41 and numberAllTasks % 2 == 0:
                        motivation="Horay! Another task done! Don't slow down!"
                    # even values and < 50%
                    if 0.4 < rainbowValue < 0.5 and numberAllTasks % 2 == 0:
                        motivation="Great job, You! You are beating this game!"
                    # 50%
                    if rainbowValue == 0.5:
                        motivation="Just halfway to have things done!! You are amazing!"
                    # odd values and > 50%
                    if rainbowValue > 0.5 and numberAllTasks % 2 !=0:
                        motivation="You have passed halfway line! You are a star!!"
                    #odd values and > 60%
                    if rainbowValue > 0.6 and numberAllTasks % 2 !=0:
                        motivation="Horay! Another task done! Don't slow down!"
                    #odd values and > 70%
                    if rainbowValue > 0.7 and numberAllTasks % 2 !=0:
                        motivation="Great job, You! You are beating this game!"
                    # even values and > 50%
                    if rainbowValue > 0.5 and numberAllTasks % 2 == 0:
                        motivation="You have passed halfway line! You are a star!!"
                    # even values and > 60%
                    if rainbowValue > 0.6 and numberAllTasks % 2 == 0:
                        motivation="Horay! Another task done! Don't slow down!"
                    # even values and > 70%
                    if rainbowValue > 0.7 and numberAllTasks % 2 == 0:
                        motivation="Great job, You! You are beating this game!"
                    # X-2/X
                    if numberDoneTasks + 2 == numberAllTasks:
                        motivation="You are a beast when it comes to completing tasks! the last two ahead!"
                    # X-1/X
                    if numberDoneTasks + 1 == numberAllTasks:
                        motivation="Great job you! One last task to do! Go ahead!!! "
                    # 100%
                    if numberAllTasks == numberDoneTasks:
                        motivation="Congratulation! You are simply the best! Everything is done! Enjoy the moment and your free time!"
                # card completed***********************************
                if numberAllTasks > 0:
                    if numberAllTasks == numberDoneTasks:
                        print('Great job')
                        print(cardForToday.completed)
                        cardForToday.completed = True
                        award = Award( title="Day Award", image="award.png", card_id=cardForToday.id)
                        db.session.add(award)
                        db.session.commit()
                        print('Great job -  changed')
                        print(cardForToday.completed)
                        return redirect(url_for('completed')) 
                print("Todays card is:",cardForToday.header)
                print ("Number of all tasks = ", numberAllTasks)
                print ("Number of done tasks = ", numberDoneTasks)
                print ("Rainbow value = ", rainbowValue)
                print ("Random choice = ", random.choice(allTasksForToday))

        if cardForToday.completed == True:
            rainbowMeter = 0
            
    #quote__________________________
    # note! quotes are numbered from 2 to 32
    allQuotes = Quote.query.all()
    quoteForToday = random.choice(allQuotes)
    allAwards = Award.query.all()
    print('AWAAAAAAAAAAAAAAAAAAAAAARRRRRDDDDDSSSSSSSS')
    print(allAwards)




    

    return render_template('thisboard.html', user=user, title=thisboard.title, motivation=motivation, boards=boards, formCard=formCard, cards=cards, 
    formTask=formTask, tasks=tasks, formDeleteTask=formDeleteTask, formDeleteCard=formDeleteCard, formDoneTask=formDoneTask, allTasksForToday=allTasksForToday,
    doneTasksForToday=doneTasksForToday, rainbowValue=rainbowValue, rainbowMeter=rainbowMeter, quoteForToday=quoteForToday)

@app.route("/completed", methods=['GET', 'POST'])
@login_required
def completed():

    return render_template('completed.html', title='Your Award')

@app.route("/awards")
@login_required
def awards():
    user = current_user
    # allAwards = Award.query.all()
    allAwards = db.session.query(Award.title, Award.card_id, Card, Board).select_from(Award).join(Card).join(Board).filter(Board.user_id == user.id).all()
    print(allAwards)
   
    for award in allAwards:
        awardtitle = award.title
        # this would be ideal solution !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # awardedCard = Card.query.filter_by(id=award.card_id).first()
        # awd = str(awardedCard.date)
        # print(awd)
    allCompletedCard = db.session.query(Card.date, Board).join(Board).filter(Card.completed == True).filter(Board.user_id == user.id).order_by(Card.date).all()
    print("completed cards:")
    print(allCompletedCard)

   
    return render_template('awards.html', title='My Awards Gallery', awardtitle=awardtitle, allAwards=allAwards , award=award)

@app.route("/reports")
@login_required
def reports():
    user = current_user
    today = date.today()
    #week
    today = today - timedelta(days= 0)
    weekday = today.weekday()
    mon = today + timedelta(days=(0 - weekday))
    tue = today + timedelta(days=(1 - weekday))
    wed = today + timedelta(days=(2 - weekday))
    thu = today + timedelta(days=(3 - weekday))
    fri = today + timedelta(days=(4 - weekday))
    sat = today + timedelta(days=(5 - weekday))
    sun = today + timedelta(days=(6 - weekday))
    delta = sun - mon
    week = [mon, tue, wed, thu, fri, sat, sun]
    dayname = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
   
    # ratioweek = [monrat, tuerat, wedrat, thurat, frirat, satrat,]
    ratiorange = range(0,7)


    for i in range(0,7):
        day = mon +timedelta(days=i)
        whichday = dayname[i]
        # numbers
        analyticsDone = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==day).filter(Task.done == True).filter(Board.user_id == user.id).all()
        analyticsAll = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==day).filter(Board.user_id == user.id).all()
        numberDone = len(analyticsDone)
        numberAll = len(analyticsAll)
        if numberAll > 0:
            ratio = numberDone/numberAll
        if numberAll == 0:
            ratio = 0
        graph= 180*ratio
        print('DOOONE_________________/ GRAPH')
        print(numberDone, graph)
        print('ALLL_________________/RATIO')
        print(numberAll, ratio)

    # monday
    analyticsDone = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==mon).filter(Task.done == True).filter(Board.user_id == user.id).all()
    analyticsAll = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==mon).filter(Board.user_id == user.id).all()
    numberDone = len(analyticsDone)
    numberAll = len(analyticsAll)
    if numberAll > 0:
        ratio_mon = numberDone/numberAll
    if numberAll == 0:
        ratio_mon = 0
    ratio_mon = int(round(ratio_mon, 2)*100)

    # tuesday
    analyticsDone = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==tue).filter(Task.done == True).filter(Board.user_id == user.id).all()
    analyticsAll = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==tue).filter(Board.user_id == user.id).all()
    numberDone = len(analyticsDone)
    numberAll = len(analyticsAll)
    if numberAll > 0:
        ratio_tue = numberDone/numberAll
    if numberAll == 0:
        ratio_tue = 0
    ratio_tue = int(round(ratio_tue, 2)*100)

    # wednesday
    analyticsDone = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==wed).filter(Task.done == True).filter(Board.user_id == user.id).all()
    analyticsAll = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==wed).filter(Board.user_id == user.id).all()
    numberDone = len(analyticsDone)
    numberAll = len(analyticsAll)
    if numberAll > 0:
        ratio_wed = numberDone/numberAll
    if numberAll == 0:
        ratio_wed = 0
    ratio_wed = int(round(ratio_wed, 2)*100)

    # thursday
    analyticsDone = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==thu).filter(Task.done == True).filter(Board.user_id == user.id).all()
    analyticsAll = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==thu).filter(Board.user_id == user.id).all()
    numberDone = len(analyticsDone)
    numberAll = len(analyticsAll)
    if numberAll > 0:
        ratio_thu = numberDone/numberAll
    if numberAll == 0:
        ratio_thu = 0
    ratio_thu = int(round(ratio_thu, 2)*100)

    # friday
    analyticsDone = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==fri).filter(Task.done == True).filter(Board.user_id == user.id).all()
    analyticsAll = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==fri).filter(Board.user_id == user.id).all()
    numberDone = len(analyticsDone)
    numberAll = len(analyticsAll)
    if numberAll > 0:
        ratio_fri = numberDone/numberAll
    if numberAll == 0:
        ratio_fri = 0
    ratio_fri = int(round(ratio_fri, 2)*100)

    # saturday
    analyticsDone = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==sat).filter(Task.done == True).filter(Board.user_id == user.id).all()
    analyticsAll = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==sat).filter(Board.user_id == user.id).all()
    numberDone = len(analyticsDone)
    numberAll = len(analyticsAll)
    if numberAll > 0:
        ratio_sat = numberDone/numberAll
    if numberAll == 0:
        ratio_sat = 0
    ratio_sat = int(round(ratio_sat, 2)*100)

    # sunday
    analyticsDone = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==sun).filter(Task.done == True).filter(Board.user_id == user.id).all()
    analyticsAll = db.session.query( Task.done, Card.date, Board).select_from(Task).join(Card).join(Board).filter(Card.date==sun).filter(Board.user_id == user.id).all()
    numberDone = len(analyticsDone)
    numberAll = len(analyticsAll)
    if numberAll > 0:
        ratio_sun = numberDone/numberAll
    if numberAll == 0:
        ratio_sun = 0
    ratio_sun = int(round(ratio_sun, 2)*100)
    

    weekratio = [ratio_mon, ratio_tue, ratio_wed, ratio_thu, ratio_fri, ratio_sat, ratio_sun ]


    user = current_user
    return render_template('reports.html', title='My Analytics', day=day, week=week, whichday=whichday, dayname=dayname, graph=graph, ratio=ratio, weekratio=weekratio)

@app.route("/test")
def test():
    # return app.config['SECRET_KEY']
    user = current_user
    displayBoard = user.boards.all()
    # sss = Board.query.filter_by(title="New Board")


    return render_template('testboard.html', boards=displayBoard, user=user, title='test', greeting="Let's do it!")


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors.html'), 500
