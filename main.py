import os
from flask import Flask, render_template, request, session
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = "I_DONT_NEED_IT"
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    logins = db.Column(db.Integer)
    exercise_generated = db.Column(db.Integer)
    

    def __init__(self, username, logins, exercise_generated):
        self.username = username
        self.logins = logins
        self.exercise_generated = exercise_generated

    def __str__(self):
        return '<User %r>' % [self.username, self.logins, self.exercise_generated]

data = [
  {
    "name": "Incline Hammer Curls",
    "type": "strength",
    "muscle": "biceps",
    "image": "https://static.strengthlevel.com/images/illustrations/incline-hammer-curl-1000x1000.jpg",
    "equipment": "dumbbell",
    "difficulty": "beginner",
    "instructions": "Seat yourself on an incline bench with a dumbbell in each hand. You should pressed firmly against he back with your feet together. Allow the dumbbells to hang straight down at your side, holding them with a neutral grip. This will be your starting position. Initiate the movement by flexing at the elbow, attempting to keep the upper arm stationary. Continue to the top of the movement and pause, then slowly return to the start position."
  },
  {
    "name": "Wide-grip barbell curl",
    "type": "strength",
    "muscle": "biceps",
    "image": "https://images.squarespace-cdn.com/content/v1/5ffcea9416aee143500ea103/1638183377952-LJZ8PDJYO558HFQV31KX/Standing%2BEZ%2BBar%2BCurls.jpeg?format=300w",
    "equipment": "barbell",
    "difficulty": "beginner",
    "instructions": "Stand up with your torso upright while holding a barbell at the wide outer handle. The palm of your hands should be facing forward. The elbows should be close to the torso. This will be your starting position. While holding the upper arms stationary, curl the weights forward while contracting the biceps as you breathe out. Tip: Only the forearms should move. Continue the movement until your biceps are fully contracted and the bar is at shoulder level. Hold the contracted position for a second and squeeze the biceps hard. Slowly begin to bring the bar back to starting position as your breathe in. Repeat for the recommended amount of repetitions.  Variations:  You can also perform this movement using an E-Z bar or E-Z attachment hooked to a low pulley. This variation seems to really provide a good contraction at the top of the movement. You may also use the closer grip for variety purposes."
  },
  {
    "name": "EZ-bar spider curl",
    "type": "strength",
    "muscle": "biceps",
    "image": "https://s3.amazonaws.com/prod.skimble/assets/1928073/image_iphone.jpg",
    "equipment": "barbell",
    "difficulty": "intermediate",
    "instructions": "Start out by setting the bar on the part of the preacher bench that you would normally sit on. Make sure to align the barbell properly so that it is balanced and will not fall off. Move to the front side of the preacher bench (the part where the arms usually lay) and position yourself to lay at a 45 degree slant with your torso and stomach pressed against the front side of the preacher bench. Make sure that your feet (especially the toes) are well positioned on the floor and place your upper arms on top of the pad located on the inside part of the preacher bench. Use your arms to grab the barbell with a supinated grip (palms facing up) at about shoulder width apart or slightly closer from each other. Slowly begin to lift the barbell upwards and exhale. Hold the contracted position for a second as you squeeze the biceps. Slowly begin to bring the barbell back to the starting position as your breathe in. . Repeat for the recommended amount of repetitions.  Variation: You can also use dumbbells when performing this exercise. Just make sure you place the dumbbells on the part of the preacher bench where you would normally sit properly."
  },
  {
    "name": "Hammer Curls",
    "type": "strength",
    "muscle": "biceps",
    "image": "https://cdn.shopify.com/s/files/1/1876/4703/files/shutterstock_419477203_480x480.jpg?v=1636560233",
    "equipment": "dumbbell",
    "difficulty": "intermediate",
    "instructions": "Stand up with your torso upright and a dumbbell on each hand being held at arms length. The elbows should be close to the torso. The palms of the hands should be facing your torso. This will be your starting position. Now, while holding your upper arm stationary, exhale and curl the weight forward while contracting the biceps. Continue to raise the weight until the biceps are fully contracted and the dumbbell is at shoulder level. Hold the contracted position for a brief moment as you squeeze the biceps. Tip: Focus on keeping the elbow stationary and only moving your forearm. After the brief pause, inhale and slowly begin the lower the dumbbells back down to the starting position. Repeat for the recommended amount of repetitions.  Variations: There are many possible variations for this movement. For instance, you can perform the exercise sitting down on a bench with or without back support and you can also perform it by alternating arms; first lift the right arm for one repetition, then the left, then the right, etc."
  },
  {
    "name": "EZ-Bar Curl",
    "type": "strength",
    "muscle": "biceps",
    "image": "https://images.squarespace-cdn.com/content/v1/5ffcea9416aee143500ea103/1638183377952-LJZ8PDJYO558HFQV31KX/Standing%2BEZ%2BBar%2BCurls.jpeg?format=300w",
    "equipment": "e-z_curl_bar",
    "difficulty": "intermediate",
    "instructions": "Stand up straight while holding an EZ curl bar at the wide outer handle. The palms of your hands should be facing forward and slightly tilted inward due to the shape of the bar. Keep your elbows close to your torso. This will be your starting position. Now, while keeping your upper arms stationary, exhale and curl the weights forward while contracting the biceps. Focus on only moving your forearms. Continue to raise the weight until your biceps are fully contracted and the bar is at shoulder level. Hold the top contracted position for a moment and squeeze the biceps. Then inhale and slowly lower the bar back to the starting position. Repeat for the recommended amount of repetitions.  Variations: You can also perform this movement using an E-Z attachment hooked to a low pulley. This variation seems to really provide a good contraction at the top of the movement. You may also use the closer grip for variety purposes."
  },
  {
    "name": "Zottman Curl",
    "type": "strength",
    "muscle": "biceps",
    "image": "https://bodybuilding-wizard.com/wp-content/uploads/2015/08/standing-zottman-curl-exercise-guide-1-2.jpg",
    "equipment": "None",
    "difficulty": "intermediate",
    "instructions": "Stand up with your torso upright and a dumbbell in each hand being held at arms length. The elbows should be close to the torso. Make sure the palms of the hands are facing each other. This will be your starting position. While holding the upper arm stationary, curl the weights while contracting the biceps as you breathe out. Only the forearms should move. Your wrist should rotate so that you have a supinated (palms up) grip. Continue the movement until your biceps are fully contracted and the dumbbells are at shoulder level. Hold the contracted position for a second as you squeeze the biceps. Now during the contracted position, rotate your wrist until you now have a pronated (palms facing down) grip with the thumb at a higher position than the pinky. Slowly begin to bring the dumbbells back down using the pronated grip. As the dumbbells close your thighs, start rotating the wrist so that you go back to a neutral (palms facing your body) grip. Repeat for the recommended amount of repetitions."
  },
  {
    "name": "Biceps curl to shoulder press",
    "type": "strength",
    "muscle": "biceps",
    "image": "https://as2.ftcdn.net/v2/jpg/03/54/12/43/1000_F_354124322_HjOlzG5NE7nhSP8AoG2djLcE2C5OP0xW.jpg",
    "equipment": "dumbbell",
    "difficulty": "beginner",
    "instructions": "Begin in a standing position with a dumbbell in each hand. Your arms should be hanging at your sides with your palms facing forward. Look directly ahead, keeping your chest up, with your feet shoulder-width apart. This will be your starting position. Initiate the movement by flexing the elbows to curl the weight. Do not use momentum or flex through the shoulder, instead use a controlled motion. Execute the pressing movement by extending the arm, flexing and abducting the shoulder to rotate the arm as you press above your head. Pause at the top of the motion before reversing the movement to return to the starting position. Complete the desired number of repetitions before switching to the opposite side."
  },
  {
    "name": "Barbell Curl",
    "type": "strength",
    "muscle": "biceps",
    "image": "https://cdn.shopify.com/s/files/1/1497/9682/articles/2_73c5a35b-aa8c-45ff-8ef1-8d074ed9c16d.jpg?v=1648742110",
    "equipment": "barbell",
    "difficulty": "intermediate",
    "instructions": "Stand up with your torso upright while holding a barbell at a shoulder-width grip. The palm of your hands should be facing forward and the elbows should be close to the torso. This will be your starting position. While holding the upper arms stationary, curl the weights forward while contracting the biceps as you breathe out. Tip: Only the forearms should move. Continue the movement until your biceps are fully contracted and the bar is at shoulder level. Hold the contracted position for a second and squeeze the biceps hard. Slowly begin to bring the bar back to starting position as your breathe in. Repeat for the recommended amount of repetitions.  Variations:  You can also perform this movement using a straight bar attachment hooked to a low pulley. This variation seems to really provide a good contraction at the top of the movement. You may also use the closer grip for variety purposes."
  },
  {
    "name": "Concentration curl",
    "type": "strength",
    "muscle": "biceps",
    "image": "https://static.strengthlevel.com/images/illustrations/dumbbell-concentration-curl-1000x1000.jpg",
    "equipment": "dumbbell",
    "difficulty": "intermediate",
    "instructions": "Sit down on a flat bench with one dumbbell in front of you between your legs. Your legs should be spread with your knees bent and feet on the floor. Use your right arm to pick the dumbbell up. Place the back of your right upper arm on the top of your inner right thigh. Rotate the palm of your hand until it is facing forward away from your thigh. Tip: Your arm should be extended and the dumbbell should be above the floor. This will be your starting position. While holding the upper arm stationary, curl the weights forward while contracting the biceps as you breathe out. Only the forearms should move. Continue the movement until your biceps are fully contracted and the dumbbells are at shoulder level. Tip: At the top of the movement make sure that the little finger of your arm is higher than your thumb. This guarantees a good contraction. Hold the contracted position for a second as you squeeze the biceps. Slowly begin to bring the dumbbells back to starting position as your breathe in. Caution: Avoid swinging motions at any time. Repeat for the recommended amount of repetitions. Then repeat the movement with the left arm.  Variations: This exercise can be performed standing with the torso bent forward and the arm in front of you. In this case, no leg support is used for the back of your arm so you will need to make extra effort to ensure no movement of the upper arm. This is a more challenging version of the exercise and is not recommended for people with lower back issues."
  },
  {
    "name": "Flexor Incline Dumbbell Curls",
    "type": "strength",
    "muscle": "biceps",
    "image": "https://www.oxygenmag.com/wp-content/uploads/2014/01/inclinebencha-b-1.jpg?crop=535:301&width=1070&enable=upscale",
    "equipment": "dumbbell",
    "difficulty": "beginner",
    "instructions": "Hold the dumbbell towards the side farther from you so that you have more weight on the side closest to you. (This can be done for a good effect on all bicep dumbbell exercises). Now do a normal incline dumbbell curl, but keep your wrists as far back as possible so as to neutralize any stress that is placed on them. Sit on an incline bench that is angled at 45-degrees while holding a dumbbell on each hand. Let your arms hang down on your sides, with the elbows in, and turn the palms of your hands forward with the thumbs pointing away from the body. Tip: You will keep this hand position throughout the movement as there should not be any twisting of the hands as they come up. This will be your starting position. Curl up the two dumbbells at the same time until your biceps are fully contracted and exhale. Tip: Do not swing the arms or use momentum. Keep a controlled motion at all times. Hold the contracted position for a second at the top. As you inhale, slowly go back to the starting position. Repeat for the recommended amount of repetitions.  Caution: Do not extend your arms totally as you could injure your elbows if you hyperextend them. Also, make sure that on the way down you move slowly to avoid injury. Variations: You can use cables for this movement as well."
  }
]

last_exercise = {}
if "last_exercise" not in last_exercise:
    last_exercise["last_exercise"] = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_name = request.form['user_name']
        session["user"] = user_name
        user = create_or_update(user_name)
    
    else:
        user = None
    
    return render_template("index.html", 
    total_excercise = total_exercise(),
    exercise_img = last_exercise["last_exercise"], 
    users = enumerate(get_leaderboard(User.query.all())), user=user)


@app.route('/exercise')
def exercise_info(exercise = last_exercise["last_exercise"] ):
  n_ex = []
  for last_es in last_exercise["last_exercise"]:
    n_ex.append(last_es)
  return render_template("exercise.html", ex_info = n_ex)


@app.route('/get_exercise')
def get_excercise():
    exercise = random.choice(data)
    last_exercise["last_exercise"] = exercise["image"], exercise["name"], exercise["type"], exercise["muscle"], exercise["difficulty"], exercise["instructions"], exercise["equipment"]


    if session['user']:
        user = get_user_from_database(session['user'])
        user.exercise_generated += 1

    return render_template("index.html", 
    exercise_img = exercise["image"],
    exercise_info = last_exercise["last_exercise"],
    users = enumerate(get_leaderboard(User.query.all())), 
    user=user,
    total_excercise = total_exercise(), exercise=exercise
    )

@app.route('/logout')
def logout():
    session['user'] = None
    return render_template("index.html")

def create_or_update(user_name):
    user = get_user_from_database(user_name)

    if user:
            # print("User exists")
            user.logins += 1
            # print(user)

    else:
        user = User(user_name, logins=1, exercise_generated=0)
        db.session.add(user)
        db.session.commit()
        user = get_user_from_database(user_name)
    return user

def get_user_from_database(user_name):
    user = [user for user in User.query.filter_by(username=user_name).all() if user.username == user_name]
    return user[0] if user else None

def total_exercise():
    users = User.query.all()
    count = 0
    for user in users:
        count += user.exercise_generated
    return count

def get_leaderboard(users):
    return sorted(User.query.all(), key= lambda user:user.exercise_generated, reverse=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
# debug=True,host='0.0.0.0', port=81