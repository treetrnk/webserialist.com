from flask import render_template, redirect, flash, url_for, current_app, request, session
from app import db
from app.main import bp
from flask_login import login_required, current_user
from app.auth.authenticators import group_required
from app.main.generic_views import SaveObjView, DeleteObjView
from app.main.forms import FictionEditForm, SubscribeForm, SubmissionEditForm, FictionSearchForm, LinkAddForm
from app.models import Fiction, Subscriber, View, Rating, Submission, Genre, Tag, Link
from sqlalchemy import func

# Add routes here
@bp.route('/fiction/<int:obj_id>/rate/<int:stars>')
@login_required
def rate(obj_id, stars):
    current_app.logger.debug(stars)
    fiction = Fiction.query.filter_by(id=obj_id).first()
    if not fiction or not stars:
        flash('That fiction does not exist', 'danger')
        return index()
    rating = Rating.query.filter_by(user_id=current_user.id, fiction_id=obj_id).first()
    if rating:
        rating.stars = stars
        flash('Your rating has been updated.', 'success')
    else:
        rating = Rating(
                stars = stars,
                user_id = current_user.id,
                fiction_id = obj_id,
            )
        db.session.add(rating)
        flash('Your rating has been added.', 'success')
    fiction.update_rating()
    db.session.commit()
    return redirect(url_for('main.fiction', obj_id=fiction.id))

@bp.route('/genre/<string:genre>')
@login_required # DELETE WHEN READY
def genre_fictions(genre):
    genre = Genre.query.filter(func.lower(Genre.name) == func.lower(genre)).first()
    if not genre:
        return redirect(url_for('main.404'))
    return render_template('main/genre_fiction.html',
                genre=genre,
            )

@bp.route('/fiction/<int:obj_id>')
@bp.route('/fiction/<int:obj_id>/<string:slug>')
@login_required # DELETE WHEN READY
def fiction(obj_id, slug=''):
    #fiction = Fiction.query.filter_by(id=obj_id, approval=True).first()
    fiction = Fiction.query.filter_by(id=obj_id).first()
   
    current_app.logger.debug(session)
    current_app.logger.debug(session.get('_id'))

    session_id = session.get('_id')

    view = View(
       fiction_id = fiction.id,
       session_id = session_id,
    )
    if current_user.is_authenticated:
        view.user_id = current_user.id
    db.session.add(view)
    db.session.commit()
    current_app.logger.debug(f'Fiction: {fiction}')

    rating = None
    if current_user.is_authenticated:
        rating = Rating.query.filter_by(user_id=current_user.id,fiction_id=fiction.id).first()

    current_app.logger.debug('VIEWS')
    current_app.logger.debug(fiction.total_views)
    return render_template('main/fiction.html',
            fiction=fiction,
            rating=rating,
        )

@bp.route('/top')
@login_required # DELETE WHEN READY
def top_stories(source=None, sort=None):
    top_rated = Fiction.query.order_by(Fiction.rating_average.desc()).limit(10).all()
    popular_fictions = Fiction.query.order_by(Fiction.weekly_views.desc()).all()
    voted_fictions = Fiction.query.order_by(Fiction.weekly_votes.desc()).all()
    random_fictions = Fiction.query.order_by(func.random()).all()
    if sort == 'random':
        fictions = Fiction.query.order_by(func.random()).all()
    else:
        fictions = Fiction.query.all()
        sort = 'trending'
    title = 'Top Stories'
    if sort:
        title += ' - ' + sort
    return render_template('main/top.html',
                title = 'Top Stories',
                fictions = fictions,
                sort = sort,
                top_rated=top_rated,
                popular_fictions=popular_fictions,
                voted_fictions=voted_fictions,
                random_fictions=random_fictions,

        )

@bp.route('/top/random')
def top_random():
    return top_stories(sort='random')

@bp.route('/fiction/search')
@login_required # DELETE WHEN READY
def fiction_search():
    form = FictionSearchForm()

    sort = request.args.get('sort')
    genres = request.args.get('genres') or ''
    tags = request.args.get('tags') or ''
    keywords = request.args.get('keywords') or ''
    current_app.logger.debug(genres)
    
    form.sort.data = sort
    form.genres.data = genres
    form.tags.data = tags
    form.keywords.data = keywords
    
    sort_order = sort.split(',') if sort else None
    sort = sort_order[0] if sort else 'rating'
    order = sort_order[1] if sort_order and len(sort_order) > 1 else 'desc'
    genres = genres.split(',')
    genres = [g for g in genres if g]
    tags = tags.split(',')
    tags = [t for t in tags if t]
    #keywords = keywords.split(' ')
    #keywords = [k for k in keywords if k]

    fictions = Fiction.query
    if genres:
        current_app.logger.debug('GENRES')
        current_app.logger.debug(genres)
        fictions = fictions.filter(Fiction.genres.any(Genre.name.in_(genres)))
    if tags:
        current_app.logger.debug('TAGS')
        current_app.logger.debug(tags)
        fictions = fictions.filter(Fiction.tags.any(Tag.name.in_(tags)))
    if keywords:
        current_app.logger.debug('KEYWORDS')
        current_app.logger.debug(keywords)
        fictions = fictions.filter(Fiction.synopsis.ilike("%" + keywords + "%"))
    if sort:
        if sort == 'rating':
            if order == 'asc':
                fictions = fictions.order_by('rating', 'title', 'approval_date')
            else:
                fictions = fictions.order_by(Fiction.rating.desc(), 'title', 'approval_date')
        elif sort == 'votes':
            pass
        elif sort == 'views':
            if order == 'asc':
                fictions = fictions.order_by('votes', 'title', 'approval_date')
            else:
                fictions = fictions.order_by(Fiction.votes.desc(), 'title', 'approval_date')
        elif sort == 'random':
            fictions = fictions.order_by(func.random())

    form.genres.choices = [(g.name, g.name) for g in Genre.query.all()]
    form.tags.choices = [(t.name, t.name) for t in Tag.query.all()]
    form.sort.choices = Fiction.SEARCH_SORT_CHOICES

    return render_template('main/fiction_search.html',
                fictions=fictions.all(),
                form=form,
            )



@bp.route('/landing-page')
def landing_page():
    return render_template('index.html')

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return top_stories()
    return landing_page()

@bp.route('/submissions')
@login_required
def submissions():
    submissions = Submission.query.filter_by(submitter_id=current_user.id).order_by(Submission.approval_date.desc()).all()
    return render_template('main/submissions.html',
            submissions=submissions,
        )

class AddSubmission(SaveObjView):
    title = "Add Submission"
    model = Submission
    form = SubmissionEditForm
    action = 'Add'
    log_msg = 'added a submission'
    success_msg = 'Submission added.'
    delete_endpoint = 'main.delete_submission'
    template = 'object-edit.html'
    redirect = {'endpoint': 'auth.profile'}

    def extra(self):
        current_app.logger.debug(self.form.__dict__)
        self.form.status.choices = Fiction.STATUS_CHOICES
        self.form.rating.choices = Fiction.RATING_CHOICES
    
    def pre_post(self):
        for entry in self.form.links.entries:
            self.obj.links.append(Link())

    def post_post(self):
        if self.form.author_claim.data == True:
            self.obj.author_id = current_user.id
        self.obj.updater_id = current_user.id
        self.obj.submitter_id = current_user.id

bp.add_url_rule("/submission/add", 
        view_func=login_required(AddSubmission.as_view('add_submission')))

class EditSubmission(SaveObjView):
    title = "Edit Submission"
    model = Submission
    form = SubmissionEditForm
    action = 'Edit'
    log_msg = 'updated a submission'
    success_msg = 'Submission updated.'
    delete_endpoint = 'main.delete_submission'
    template = 'object-edit.html'
    add_child_endpoint = 'main.add_submission_link'
    redirect = {'endpoint': 'auth.profile'}

    def extra(self):
        self.form.status.choices = Fiction.STATUS_CHOICES
        self.form.rating.choices = Fiction.RATING_CHOICES

    #def pre_post(self):
    #    for entry in self.form.links.entries:
    #        self.obj.links.append(Link())

bp.add_url_rule("/submission/edit/<int:obj_id>", 
        view_func=login_required(EditSubmission.as_view('edit_submission')))

class DeleteSubmission(DeleteObjView):
    model = Submission
    log_msg = 'deleted a submission'
    success_msg = 'Submission deleted.'
    redirect = {'endpoint': 'main.profile'}

bp.add_url_rule("/submission/delete", 
        view_func = login_required(DeleteSubmission.as_view('delete_submission')))

class AddSubmissionLink(SaveObjView):
    title = "Add Submission Link"
    model = Link
    form = LinkAddForm
    action = 'Add'
    log_msg = 'added a submission link'
    success_msg = 'Submission link added.'
    delete_endpoint = 'main.delete_link'
    template = 'object-edit.html'
    redirect = {'endpoint': 'auth.profile'}

    def extra(self):
        self.form.fiction_id.data = self.parent_id

bp.add_url_rule("/submission/link/add", 
        view_func=login_required(AddSubmissionLink.as_view('add_submission_link')))

class AddFiction(SaveObjView):
    title = "Add Fiction"
    model = Fiction
    form = FictionEditForm
    action = 'Add'
    log_msg = 'added a fiction'
    success_msg = 'Fiction added.'
    delete_endpoint = 'main.delete_fiction'
    template = 'object-edit.html'
    redirect = {'endpoint': 'auth.profile'}

    def extra(self):
        current_app.logger.debug(self.form.__dict__)
        self.form.status.choices = Fiction.STATUS_CHOICES
    
    def pre_post(self):
        for entry in self.form.links.entries:
            self.obj.links.append(Link())

    def post_post(self):
        if self.form.author_claim.data == True:
            self.obj.author_id = current_user.id
        self.obj.updater_id = current_user.id

bp.add_url_rule("/fiction/add", 
        view_func=group_required('admin')(AddFiction.as_view('add_fiction')))

class EditFiction(SaveObjView):
    title = "Edit Fiction"
    model = Fiction
    form = FictionEditForm
    action = 'Edit'
    log_msg = 'updated a fiction'
    success_msg = 'Fiction updated.'
    delete_endpoint = 'main.delete_fiction'
    template = 'object-edit.html'
    redirect = {'endpoint': 'auth.profile'}

    def extra(self):
        self.form.status.choices = Fiction.STATUS_CHOICES

bp.add_url_rule("/fiction/edit/<int:obj_id>", 
        view_func=group_required('admin')(EditFiction.as_view('edit_fiction')))

class DeleteFiction(DeleteObjView):
    model = Fiction
    log_msg = 'deleted a fiction'
    success_msg = 'Fiction deleted.'
    redirect = {'endpoint': 'main.profile'}

bp.add_url_rule("/fiction/delete", 
        view_func = group_required('admin')(DeleteFiction.as_view('delete_fiction')))

class AddSubscriber(SaveObjView):
    decorators = []
    title = "Subscribe"
    model = Subscriber
    form = SubscribeForm
    action = 'Add'
    log_msg = 'added a subscriber'
    success_msg = 'Subscriber added.'
    delete_endpoint = 'main.delete_subscriber'
    template = 'object-edit.html'
    redirect = {'endpoint': 'main.index'}

bp.add_url_rule("/subscribe", 
        view_func=AddSubscriber.as_view('subscribe'))

class DeleteSubscriber(DeleteObjView):
    model = Subscriber
    log_msg = 'deleted a subscriber'
    success_msg = 'Subscriber deleted.'
    redirect = {'endpoint': 'main.index'}

bp.add_url_rule("/unsubscribe", 
        view_func = login_required(DeleteSubscriber.as_view('unsubscribe')))

@bp.app_errorhandler(404)
@login_required
def handle_404(e):
    return render_template("404-error.html", title="Page not found")

@bp.app_errorhandler(500)
@login_required
def handle_500(e):
    return render_template("500-error.html", title="Internal Server Error", error=e)
