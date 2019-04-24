
from flask import url_for, current_app
from flask_mail import Mail, Message


def send_mail(subject, to, html):
    message = Message(subject, recipients=[to], body=html)
    mail = Mail(current_app)
    mail.send(message)


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comment'
    send_mail(subject='New comment', to=current_app.config['BLUELOG_ADMIN_EMAIL'],
              html='<p>New comment in post <i> %s </i>, click the link below to check:</p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">Do no reply this email.</small></p>'
                   % (post.title, post_url, post_url)
              )


def send_reply_new_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.id, _external=True) + '#comments'
    send_mail(subject='New reply', to=comment.email,
              html='<p>New reply for the comment you left in post <i>%s</i> click the link below to check; </p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96"></small>Do not reply this email.</p>'
                   % (comment.title, post_url, post_url)
              )

