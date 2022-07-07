from flask import session
from app.app import create_app
from app.deck_pages.models import Deck, Card, Image
from app.users.models import User
from app.extensions.database import db
import base64
from datetime import datetime, timedelta

app = create_app()
app.app_context().push()

decks_data = [
    {"title": "CS", "color": "#F3B700", "date_created": datetime.utcnow() + timedelta(minutes=1), "user_id": 1},
    {"title": "Math","color": "#61E8E1", "date_created": datetime.utcnow() + timedelta(minutes=2), "user_id": 1},
    {"title": "Chemistry","color": "#F25757", "date_created": datetime.utcnow() + timedelta(minutes=3), "user_id": 1},
    ]

cards_data = [   
    {
        "title": "CS Card 1",
        "content": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Illa tamen simplicia, vestra versuta. Comprehensum, quod cognitum non habet? Utram tandem linguam nescio? <i>An hoc usque quaque, aliter in vita?</i> Duo Reges: constructio interrete. </p><ul><li>Nam, ut paulo ante docui, augendae voluptatis finis est doloris omnis amotio.</li><li>Post enim Chrysippum eum non sane est disputatum.</li></ul>",
        "date_created": datetime.utcnow() + timedelta(minutes=4),
        "deck_id": 1
    },

    {
        "title": "CS Card 2",
        "content": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Disserendi artem nullam habuit. <b>Si longus, levis.</b> </p><ul><li>Duo Reges: constructio interrete.</li><li>Tu autem negas fortem esse quemquam posse, qui dolorem malum putet.</li><li>Voluptatem cum summum bonum diceret, primum in eo ipso parum vidit, deinde hoc quoque alienum;</li><li>Quod, inquit, quamquam voluptatibus quibusdam est saepe iucundius, tamen expetitur propter voluptatem.</li></ul><p>Quo studio Aristophanem putamus aetatem in litteris duxisse? Non igitur bene.</p>",
        "date_created": datetime.utcnow() + timedelta(minutes=5),
        "deck_id": 1
    },

    {
        "title": "CS Card 3",
        "content": "",
        "date_created": datetime.utcnow() + timedelta(minutes=6),
        "deck_id": 1
    },

    {
        "title": "CS Card 4",
        "content": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Qui-vere falsone, quaerere mittimus-dicitur oculis se privasse; Quare attende, quaeso. Nondum autem explanatum satis, erat, quid maxime natura vellet. Duo Reges: constructio interrete. Qualem igitur hominem natura inchoavit? Sed ad illum redeo. An potest cupiditas finiri? Mihi, inquam, qui te id ipsum rogavi? </p><ul><li>Claudii libidini, qui tum erat summo ne imperio, dederetur.</li><li>Sin autem eos non probabat, quid attinuit cum iis, quibuscum re concinebat, verbis discrepare?</li><li>Quem si tenueris, non modo meum Ciceronem, sed etiam me ipsum abducas licebit.</li></ul>",
        "date_created": datetime.utcnow() + timedelta(minutes=7),
        "deck_id": 1
    },

    {
        "title": "Math Card 1",
        "content": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. An tu me de L. Haeret in salebra. Minime vero, inquit ille, consentit. Illi enim inter se dissentiunt. </p><ul><li>Sit hoc ultimum bonorum, quod nunc a me defenditur;</li><li>Duo Reges: constructio interrete.</li><li>His similes sunt omnes, qui virtuti student levantur vitiis, levantur erroribus, nisi forte censes Ti.</li><li>Primum in nostrane potestate est, quid meminerimus?</li></ul>",
        "date_created": datetime.utcnow() + timedelta(minutes=8),
        "deck_id": 2
    },

    {
        "title": "Math Card 2",
        "content": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. An tu me de L. Haeret in salebra. Minime vero, inquit ille, consentit. Illi enim inter se dissentiunt. </p><ul><li>Sit hoc ultimum bonorum, quod nunc a me defenditur;</li><li>Duo Reges: constructio interrete.</li><li>His similes sunt omnes, qui virtuti student levantur vitiis, levantur erroribus, nisi forte censes Ti.</li><li>Primum in nostrane potestate est, quid meminerimus?</li></ul>",
        "date_created": datetime.utcnow() + timedelta(minutes=9),
        "deck_id": 2
    },

    {
        "title": "Math Card 3",
        "content": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Restatis igitur vos; Sint ista Graecorum; <b>An potest cupiditas finiri?</b> Scio enim esse quosdam, qui quavis lingua philosophari possint; Quo modo? Pauca mutat vel plura sane; </p><ul>	<li>Semper enim ex eo, quod maximas partes continet latissimeque funditur, tota res appellatur.</li>	<li>Duo Reges: constructio interrete.</li></ul>",
        "date_created": datetime.utcnow() + timedelta(minutes=10),
        "deck_id": 2
    },

    {
        "title": "Chemistry Card 1",
        "content": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quod quidem nobis non saepe contingit. <b>Sint modo partes vitae beatae.</b> Restatis igitur vos; Duo Reges: constructio interrete. </p><ul><li>Itaque sensibus rationem adiunxit et ratione effecta sensus non reliquit.</li><li>Aliter homines, aliter philosophos loqui putas oportere?</li><li>Atque hoc dabitis, ut opinor, si modo sit aliquid esse beatum, id oportere totum poni in potestate sapientis.</li><li>Iis igitur est difficilius satis facere, qui se Latina scripta dicunt contemnere.</li></ul>",
        "date_created": datetime.utcnow() + timedelta(minutes=11),
        "deck_id": 3
    },

    {
        "title": "Chemistry Card 2",
        "content": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Eadem fortitudinis ratio reperietur. Itaque ab his ordiamur. <b>Primum quid tu dicis breve?</b> Consequentia exquirere, quoad sit id, quod volumus, effectum. </p><ul><li>Duo Reges: constructio interrete.</li><li>Minime id quidem, inquam, alienum, multumque ad ea, quae quaerimus, explicatio tua ista profecerit.</li><li>Si longus, levis.</li><li>Quae in controversiam veniunt, de iis, si placet, disseramus.</li><li>Scientiam pollicentur, quam non erat mirum sapientiae cupido patria esse cariorem.</li><li>Itaque eos id agere, ut a se dolores, morbos, debilitates repellant.</li></ul>",
        "date_created": datetime.utcnow() + timedelta(minutes=12),
        "deck_id": 3
    }
]


with open('app\static\\assets\dummy-image.png', 'rb') as image:
    image_data = base64.b64encode(image.read()).decode('utf8')

images_data = [
    {
        "data" : image_data,
        "extention": "png",
        "date_created": datetime.utcnow() + timedelta(minutes=4),
        "card_id": 1
    },

    {
        "data" : image_data,
        "extention": "png",
        "date_created": datetime.utcnow() + timedelta(minutes=6),
        "card_id": 3
    },

    {
        "data" : image_data,
        "extention": "png",
        "date_created": datetime.utcnow() + timedelta(minutes=8),
        "card_id": 5
    },

    {
        "data" : image_data,
        "extention": "png",
        "date_created": datetime.utcnow() + timedelta(minutes=12),
        "card_id": 9
    },
]
    
for deck in decks_data:
    new_deck = Deck(title = deck['title'], color = deck['color'], date_created = deck['date_created'], user_id = deck['user_id'])
    db.session.add(new_deck)

db.session.flush()

for card in cards_data:
    new_card = Card(title = card['title'], content = card['content'], date_created = card['date_created'], deck_id = card['deck_id'])
    db.session.add(new_card)

db.session.flush()

for image in images_data:
    new_card = Image(data = image['data'], extention = image['extention'], date_created = image['date_created'], card_id = image['card_id'])
    db.session.add(new_card)

db.session.flush()

db.session.commit()