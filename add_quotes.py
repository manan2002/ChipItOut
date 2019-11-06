from app import app
from exts import db
from models.quote import QuoteModel

with app.app_context():
    
    q = QuoteModel(
        text='“The greatest threat to our planet is the belief that someone else will save it.”'
        )
    q.save()
    q = QuoteModel(
        text='“Often when you think you\’re at the end of something, you’re at the beginning of something else.”'
    )
    q.save()
    q = QuoteModel(
        text='"When you put the whole picture together, recycling is the right thing to do.”'
    )
    q.save()
    q = QuoteModel(
        text='“We cannot solve our problems with the same thinking we used when we created them.”'
    )
    q.save()
    q = QuoteModel(
        text='“We do not inherit the Earth from our ancestors; we borrow it from our children.”'
    )
    q.save()
    q = QuoteModel(
        text='“We never know the worth of water till the well is dry.”'
    )
    q.save()
    q = QuoteModel(
        text='“If it can’t be reduced, reused, repaired, rebuilt, refurbished, refinished, resold, recycled, or composted, then it should be restricted, designed or removed from production.”'
    )
    q.save()
    q = QuoteModel(
        text='“We are living on this planet as if we had another one to go to.”'
    )
    q.save()
    q = QuoteModel(
        text='“At its core, the issue of a clean environment is a matter of public health.”'
    )
    q.save()


