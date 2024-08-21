from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os
import pickle
import numpy as np

art= pickle.load(open('Templates/Art_Photography.pkl','rb'))
similarity_scores= pickle.load(open('Templates/similarity_scores.pkl','rb'))
bio= pickle.load(open('Templates/Biography_df.pkl','rb'))
books= pickle.load(open('Templates/books.pkl','rb'))
busifinlaw= pickle.load(open('Templates/Business_Finance_Law_df.pkl','rb'))
child= pickle.load(open('Templates/Childrens_Books_df.pkl','rb'))
compute= pickle.load(open('Templates/Computing_df.pkl','rb'))
craft= pickle.load(open('Templates/Crafts_Hobbies_df.pkl','rb'))
crimethriller= pickle.load(open('Templates/Crime_Thriller_df.pkl','rb'))
dictionary= pickle.load(open('Templates/Dictionaries_Languages_df.pkl','rb'))
entertain= pickle.load(open('Templates/Entertainment_df.pkl','rb'))
foodd= pickle.load(open('Templates/Food_Drink_df.pkl','rb'))
graphicnovel= pickle.load(open('Templates/Graphic_Novels_Anime_Manga_df.pkl','rb'))
healthie= pickle.load(open('Templates/Health_df.pkl','rb'))
hist= pickle.load(open('Templates/History_Archaeology_df.pkl','rb'))
homeg= pickle.load(open('Templates/Home_Garden_df.pkl','rb'))
hum= pickle.load(open('Templates/Humour_df.pkl','rb'))
medi= pickle.load(open('Templates/Medical_df.pkl','rb'))
spirit= pickle.load(open('Templates/Mind_Body_Spirit_df.pkl','rb'))
nat= pickle.load(open('Templates/Natural_History_df.pkl','rb'))
personal= pickle.load(open('Templates/Personal_Development_df.pkl','rb'))
drama= pickle.load(open('Templates/Poetry_Drama_df.pkl','rb'))
pt= pickle.load(open('Templates/pt.pkl','rb'))
ref= pickle.load(open('Templates/Reference_df.pkl','rb'))
reli= pickle.load(open('Templates/Religion_df.pkl','rb'))
rom= pickle.load(open('Templates/Romance_df.pkl','rb'))
scifiction= pickle.load(open('Templates/Science_Fiction_Fantasy_Horror_df.pkl','rb'))
scig= pickle.load(open('Templates/Science_Geography_df.pkl','rb'))
sss= pickle.load(open('Templates/Society_Social_Sciences_df.pkl','rb'))
sportss= pickle.load(open('Templates/Sport_df.pkl','rb'))
stat= pickle.load(open('Templates/Stationery_df.pkl','rb'))
teachingresources= pickle.load(open('Templates/Teaching_Resources_Education_df.pkl','rb'))
techengg= pickle.load(open('Templates/Technology_Engineering_df.pkl','rb'))
tya= pickle.load(open('Templates/Teen_Young_Adult_df.pkl','rb'))
tsport=pickle.load(open('Templates/Transport_df.pkl','rb'))
travel= pickle.load(open('Templates/Travel_Holiday_Guides_df.pkl','rb'))


app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost",user="root",database="thereadingroom")
cursor=conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'database' in session:
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * FROM `database` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['database']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/add_user',methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    cursor.execute("""INSERT INTO `database` (`user_id`,`name`,`email`,`password`)
    VALUES(NULL,'{}','{}','{}')""".format(name,email,password))
    conn.commit()
    return redirect('/')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input= request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-title')['Book-title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-title')['image'].values))
        item.extend(list(temp_df.drop_duplicates('Book-title')['category'].values))

        data.append(item)

    print(data)
    return render_template('browse.html',data=data)

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/logout')
def logout():
    session.pop('database')
    return render_template('/login.html')
@app.route('/artphoto')
def artphoto():
    return render_template('Art-Photo.html',
                           book_name=list(art['Book-title'].values),
                           author=list(art['Book-Author'].values),
                           image=list(art['image'].values),
                           category=list(art['category'].values),
                           rating=list(art['rating'].values),
                           )
@app.route('/biography')
def biography():
    return render_template('Biography.html',
                           book_name=list(bio['Book-title'].values),
                           author=list(bio['Book-Author'].values),
                           image=list(bio['image'].values),
                           category=list(bio['category'].values),
                           rating=list(bio['rating'].values),
                           )
@app.route('/Businessfinlaw')
def Businessfinlaw():
    return render_template('Business-Fin-law.html',
                           book_name=list(busifinlaw['Book-title'].values),
                           author=list(busifinlaw['Book-Author'].values),
                           image=list(busifinlaw['image'].values),
                           category=list(busifinlaw['category'].values),
                           rating=list(busifinlaw['rating'].values),
                           )
@app.route('/childbook')
def childbook():
    return render_template('Childrens-Books.html',
                           book_name=list(child['Book-title'].values),
                           author=list(child['Book-Author'].values),
                           image=list(child['image'].values),
                           category=list(child['category'].values),
                           rating=list(child['rating'].values),
                           )
@app.route('/computing')
def computing():
    return render_template('Computing.html',
                           book_name=list(compute['Book-title'].values),
                           author=list(compute['Book-Author'].values),
                           image=list(compute['image'].values),
                           category=list(compute['category'].values),
                           rating=list(compute['rating'].values),
                           )
@app.route('/crafthobby')
def crafthobby():
    return render_template('Crafts-Hobbies.html',
                           book_name=list(craft['Book-title'].values),
                           author=list(craft['Book-Author'].values),
                           image=list(craft['image'].values),
                           category=list(craft['category'].values),
                           rating=list(craft['rating'].values),
                           )
@app.route('/crime')
def crime():
    return render_template('Crime-Thriller.html',
                           book_name=list(crimethriller['Book-title'].values),
                           author=list(crimethriller['Book-Author'].values),
                           image=list(crimethriller['image'].values),
                           category=list(crimethriller['category'].values),
                           rating=list(crimethriller['rating'].values),
                           )
@app.route('/dict')
def dict():
    return render_template('Dictionaries-Lang.html',
                           book_name=list(dictionary['Book-title'].values),
                           author=list(dictionary['Book-Author'].values),
                           image=list(dictionary['image'].values),
                           category=list(dictionary['category'].values),
                           rating=list(dictionary['rating'].values),
                           )
@app.route('/food')
def food():
    return render_template('Food-Drink.html',
                           book_name=list(foodd['Book-title'].values),
                           author=list(foodd['Book-Author'].values),
                           image=list(foodd['image'].values),
                           category=list(foodd['category'].values),
                           rating=list(foodd['rating'].values),
                           )
@app.route('/novel')
def novel():
    return render_template('Graphic-Novel-Anime-Manga.html',
                           book_name=list(graphicnovel['Book-title'].values),
                           author=list(graphicnovel['Book-Author'].values),
                           image=list(graphicnovel['image'].values),
                           category=list(graphicnovel['category'].values),
                           rating=list(graphicnovel['rating'].values),
                           )
@app.route('/health')
def health():
    return render_template('Health.html',
                           book_name=list(healthie['Book-title'].values),
                           author=list(healthie['Book-Author'].values),
                           image=list(healthie['image'].values),
                           category=list(healthie['category'].values),
                           rating=list(healthie['rating'].values),
                           )
@app.route('/history')
def history():
    return render_template('Hist-Archaeology.html',
                           book_name=list(hist['Book-title'].values),
                           author=list(hist['Book-Author'].values),
                           image=list(hist['image'].values),
                           category=list(hist['category'].values),
                           rating=list(hist['rating'].values),
                           )
@app.route('/homegarden')
def homegarden():
    return render_template('Home-Garden.html',
                           book_name=list(homeg['Book-title'].values),
                           author=list(homeg['Book-Author'].values),
                           image=list(homeg['image'].values),
                           category=list(homeg['category'].values),
                           rating=list(homeg['rating'].values),
                           )
@app.route('/humour')
def humour():
    return render_template('Humour.html',
                           book_name=list(hum['Book-title'].values),
                           author=list(hum['Book-Author'].values),
                           image=list(hum['image'].values),
                           category=list(hum['category'].values),
                           rating=list(hum['rating'].values),
                           )
@app.route('/medical')
def medical():
    return render_template('Mind-Body-Spirit.html',
                           book_name=list(medi['Book-title'].values),
                           author=list(medi['Book-Author'].values),
                           image=list(medi['image'].values),
                           category=list(medi['category'].values),
                           rating=list(medi['rating'].values),
                           )
@app.route('/mindbodyspirit')
def mindbodyspirit():
    return render_template('Medical.html',
                           book_name=list(spirit['Book-title'].values),
                           author=list(spirit['Book-Author'].values),
                           image=list(spirit['image'].values),
                           category=list(spirit['category'].values),
                           rating=list(spirit['rating'].values),
                           )
@app.route('/natural')
def natural():
    return render_template('Natural-History.html',
                           book_name=list(nat['Book-title'].values),
                           author=list(nat['Book-Author'].values),
                           image=list(nat['image'].values),
                           category=list(nat['category'].values),
                           rating=list(nat['rating'].values),
                           )
@app.route('/personaldevelopment')
def personaldevelopment():
    return render_template('Personal-Development.html',
                           book_name=list(personal['Book-title'].values),
                           author=list(personal['Book-Author'].values),
                           image=list(personal['image'].values),
                           category=list(personal['category'].values),
                           rating=list(personal['rating'].values),
                           )
@app.route('/reference')
def reference():
    return render_template('Reference.html',
                           book_name=list(ref['Book-title'].values),
                           author=list(ref['Book-Author'].values),
                           image=list(ref['image'].values),
                           category=list(ref['category'].values),
                           rating=list(ref['rating'].values),
                           )
@app.route('/religion')
def religion():
    return render_template('Religion.html',
                           book_name=list(reli['Book-title'].values),
                           author=list(reli['Book-Author'].values),
                           image=list(reli['image'].values),
                           category=list(reli['category'].values),
                           rating=list(reli['rating'].values),
                           )
@app.route('/romance')
def romance():
    return render_template('Romance.html',
                           book_name=list(rom['Book-title'].values),
                           author=list(rom['Book-Author'].values),
                           image=list(rom['image'].values),
                           category=list(rom['category'].values),
                           rating=list(rom['rating'].values),
                           )
@app.route('/scigeo')
def scigeo():
    return render_template('Sci-Geo.html',
                           book_name=list(scig['Book-title'].values),
                           author=list(scig['Book-Author'].values),
                           image=list(scig['image'].values),
                           category=list(scig['category'].values),
                           rating=list(scig['rating'].values),
                           )
@app.route('/scifi')
def scifi():
    return render_template('Science-Fiction-Fantasy-Horror.html',
                           book_name=list(scifiction['Book-title'].values),
                           author=list(scifiction['Book-Author'].values),
                           image=list(scifiction['image'].values),
                           category=list(scifiction['category'].values),
                           rating=list(scifiction['rating'].values),
                           )
@app.route('/socsocialscience')
def socsocialscience():
    return render_template('Society-Social-Sciences.html',
                           book_name=list(sss['Book-title'].values),
                           author=list(sss['Book-Author'].values),
                           image=list(sss['image'].values),
                           category=list(sss['category'].values),
                           rating=list(sss['rating'].values),
                           )
@app.route('/sport')
def sport():
    return render_template('Sport.html',
                           book_name=list(sportss['Book-title'].values),
                           author=list(sportss['Book-Author'].values),
                           image=list(sportss['image'].values),
                           category=list(sportss['category'].values),
                           rating=list(sportss['rating'].values),
                           )
@app.route('/stationery')
def stationery():
    return render_template('Stationery.html',
                           book_name=list(stat['Book-title'].values),
                           author=list(stat['Book-Author'].values),
                           image=list(stat['image'].values),
                           category=list(stat['category'].values),
                           rating=list(stat['rating'].values),
                           )
@app.route('/teachresource')
def teachresource():
    return render_template('Teaching-Resources-Education.html',
                           book_name=list(teachingresources['Book-title'].values),
                           author=list(teachingresources['Book-Author'].values),
                           image=list(teachingresources['image'].values),
                           category=list(teachingresources['category'].values),
                           rating=list(teachingresources['rating'].values),
                           )
@app.route('/techengi')
def techengi():
    return render_template('Technology-Engineering.html',
                           book_name=list(techengg['Book-title'].values),
                           author=list(techengg['Book-Author'].values),
                           image=list(techengg['image'].values),
                           category=list(techengg['category'].values),
                           rating=list(techengg['rating'].values),
                           )
@app.route('/teenyoungadult')
def teenyoungadult():
    return render_template('Teen-Young-Adult.html',
                           book_name=list(tya['Book-title'].values),
                           author=list(tya['Book-Author'].values),
                           image=list(tya['image'].values),
                           category=list(tya['category'].values),
                           rating=list(tya['rating'].values),
                           )
@app.route('/transport')
def transport():
    return render_template('Transport.html',
                           book_name=list(tsport['Book-title'].values),
                           author=list(tsport['Book-Author'].values),
                           image=list(tsport['image'].values),
                           category=list(tsport['category'].values),
                           rating=list(tsport['rating'].values),
                           )
@app.route('/travelholiday')
def travelholiday():
    return render_template('Travel-Holiday-Guides.html',
                           book_name=list(travel['Book-title'].values),
                           author=list(travel['Book-Author'].values),
                           image=list(travel['image'].values),
                           category=list(travel['category'].values),
                           rating=list(travel['rating'].values),
                           )

if __name__=="__main__":
    app.run(debug=True)