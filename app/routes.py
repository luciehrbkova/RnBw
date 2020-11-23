from flask import render_template, url_for, redirect, flash, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, BoardForm, CardForm, TaskForm
from flask_login import current_user, login_user
from app.models import User, Board, Card, Task
from flask_login import logout_user, login_required

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
    form = CardForm()

    # form for cards
    if form.validate_on_submit():
        cardtaken = Card.query.filter_by(date=form.date.data).filter_by(board_id=thisboardid).first()
        if cardtaken is None:
            card = Card(header=form.header.data, date=form.date.data, motherboard=thisboard)
            db.session.add(card)
            db.session.commit()
        # flash('You have only 1 card per day on your Board!')
        print('Card taken, choose another date')
        # print(card.id)
        # print("cardtaken is:")
        # print(cardtaken)
   

    

    # form for tasks
    formTask = TaskForm()
    if formTask.validate_on_submit():
        task = Task(card_id=formTask.card_id.data, tasktext=formTask.tasktext.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('board', boardid=boardid))

    cards = thisboard.cards.order_by(Card.date).all()

    for card in cards:
        # if card.id > 55:
        #     print (card.id)
        print (card.header)
        cardid= card.id
        print("tohle je card ID")
        print(cardid)
    allcardsonboard = Card.query.filter_by(board_id=thisboardid).all()
    print(allcardsonboard)
    count = Card.query.filter_by(board_id=thisboardid).count()
    print(count)

    tasks = Task.query.all()
    # print (tasks)
    print (cards)


    for card in cards:
        if card.board_id == thisboard:
            cardId = card.id
            for task in tasks:
                # if task.card_id = cardId:
                tasksOnCard = Task.query.filter_by(card_id=cardId).all()
            
            print('This is card id: !!!!!')
            print(cardId)
            print(tasksOnCard)

    

    

    return render_template('thisboard.html', user=user, title=thisboard.title, greeting="Let's do it!", boards=boards, form=form, cards=cards, formTask=formTask, tasks=tasks)


@app.route("/test")
def test():
    # return app.config['SECRET_KEY']
    user = current_user
    displayBoard = user.boards.all()
    # sss = Board.query.filter_by(title="New Board")


    return render_template('testboard.html', boards=displayBoard, user=user, title='test', greeting="Let's do it!",)

