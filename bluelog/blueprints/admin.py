
from flask import Blueprint, current_app, request, render_template, flash, redirect, url_for
from bluelog.models import Post, Category, Comment
from bluelog.forms import PostsForm, CategoryForm
from bluelog.extensions import db
from bluelog.utils import redirect_back


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/post/manage')
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by().paginate(page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', posts=posts, pagination=pagination)


@admin_bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostsForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = form.category.data
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/edit')
def edit_post(post_id):
    form = PostsForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = form.category.data
        db.session.commit()
        flash('Post Updated', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title = post.title
    form.body = post.body
    form.category = post.category
    return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/post<int:post_id>/delete')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted', 'Success')
    return redirect_back()


@admin_bp.route('/category/manage')
def manage_category():
    return render_template('admin/manage_category.html')


@admin_bp.route('/category/new')
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('.manage_category', category_id=category.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/category/<int:category_id>/edit')
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)

    if category.id != 1:
        flash('You can not edit the default category.', 'warning')
        return redirect(url_for('blog.index'))

    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category Updated', 'success')
        return redirect(url_for('.manage_category'))

    form.name = category.name
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category<int:category_id>/delete')
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not delete the default category.', 'warning')
        return redirect(url_for('blog.index'))
    category.delete()
    flash('Category Deleted', 'Success')
    return redirect('.manage_category')


@admin_bp.route('/comment/manage')
def manage_comment():
    filter_rule = request.args.get('filter', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(from_admin=True)
    else:
        filtered_comments = Comment.query

    pagination = filtered_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items

    return render_template('admin/manage_comment.html', comments=comments, pagination=pagination)


@admin_bp.route('/set-comment/<int:post_id>', methods=['GET', 'POST'])
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('Comment disabled', 'info')
    else:
        post.can_comment = True
        flash('Comment enabled', 'info')
    db.session.commit()
    return redirect(url_for('.show_post', post_id=post.id))


@admin_bp.route('/post/<int:comment_id>/delete')
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/approve')
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('Comment published.', 'success')
    return redirect_back()


@admin_bp.route('/setting')
def settings():
    pass











