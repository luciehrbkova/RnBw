from flask import render_template, url_for, redirect, flash, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, BoardForm, CardForm, TaskForm, DeleteTaskForm, DeleteCardForm, DoneTaskForm
from flask_login import current_user, login_user
from app.models import User, Board, Card, Task
from flask_login import logout_user, login_required
from datetime import date



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

@app.route("/awards")
@login_required
def awards():
    user = current_user
    return render_template('awards.html', title='My Awards Gallery')

@app.route("/reports")
@login_required
def reports():
    user = current_user
    return render_template('reports.html', title='My Analytics')

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
    form = CardForm()
    formTask = TaskForm()
    formDeleteTask = DeleteTaskForm()
    formDoneTask = DoneTaskForm()
    formDeleteCard = DeleteCardForm()
   
    # forms___________________________________________
    if request.method =='POST':
        form_name = request.form['form-name']
        if form_name == 'form-newCard':
            if form.submitc and form.validate():
                cardtaken = Card.query.filter_by(date=form.date.data).filter_by(board_id=thisboardid).first()
                if cardtaken is None:
                    card = Card(header=form.header.data, date=form.date.data, motherboard=thisboard)
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
    #CARD
    cardForToday = Card.query.filter_by(date=today).filter_by(board_id=thisboardid).first()
    #TODAYS TASKS
    allTasksForToday = Task.query.filter_by(card_id=cardForToday.id).all()
    numberAllTasks = len(allTasksForToday)
    #DONE TODAYS TASKS
    doneTasksForToday = Task.query.filter_by(card_id=cardForToday.id).filter_by(done=True).all()
    numberDoneTasks = len(doneTasksForToday)    
    #RAINBOW VALUE
    rainbowValue = numberDoneTasks/numberAllTasks

    print("Todays card is:",cardForToday.header)
    print ("Number of all tasks = ", numberAllTasks)
    print ("Number of done tasks = ", numberDoneTasks)
    print ("Rainbow value = ", rainbowValue)

    if cardForToday:
        dashboardAwardTitle = "Get award for today!"



    # for card in cards:
    #     if card.board_id == thisboard:
    #         cardId = card.id
    #         for task in tasks:
    #             # if task.card_id = cardId:
    #             tasksOnCard = Task.query.filter_by(card_id=cardId).all()
            
    #         print('This is card id: !!!!!')
    #         print(cardId)
    #         print(tasksOnCard)


  # for card in cards:
    #     # if card.id > 55:
    #     #     print (card.id)
    #     print (card.header)
    #     cardid= card.id
    #     print("tohle je card ID")
    #     print(cardid)
    # allcardsonboard = Card.query.filter_by(board_id=thisboardid).all()
    # print(allcardsonboard)
    # count = Card.query.filter_by(board_id=thisboardid).count()
    # print(count)
    

    

    return render_template('thisboard.html', user=user, title=thisboard.title, greeting="Let's do it!", boards=boards, form=form, cards=cards, 
    formTask=formTask, tasks=tasks, formDeleteTask=formDeleteTask, formDeleteCard=formDeleteCard, formDoneTask=formDoneTask, allTasksForToday=allTasksForToday,
    doneTasksForToday=doneTasksForToday)


@app.route("/test")
def test():
    # return app.config['SECRET_KEY']
    user = current_user
    displayBoard = user.boards.all()
    # sss = Board.query.filter_by(title="New Board")


    return render_template('testboard.html', boards=displayBoard, user=user, title='test', greeting="Let's do it!",)

