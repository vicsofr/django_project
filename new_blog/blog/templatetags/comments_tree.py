from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter
def comments_filter(comments_list):
    res = """
          <ul style="list-style-type:none;">
            <div class="col-md-12 mt-2"> 
            {}
            </div>
          </ul>
          """
    i = ''
    for comment in comments_list:
        i += """
             <li>
                <div class="col-md-8 mb-2 mt-2 p-0">
                    <small><i>@ {author} | {timestamp}</i></small>
                    <p></p>
                    <p>{text}</p>
                    <button type="button" class="btn btn-sm mb-3 btn-outline-secondary reply" data-id="{id}" data-parent={parent_id} >Ответить</button>
                    <form action="" method="POST" class="comment-form form-group" id="form-{id}" style="display:none;">
                        <textarea type="text" class="form-control" name="comment-text" required=True></textarea><br> 
                        <input type="submit" class="btn btn-sm mb-3 btn-outline-primary submit-reply" data-id="{id}" data-submit-reply="{parent_id}" value="Отправить">
                    </form>
                </div>
             </li>  
             """.format(id=comment['id'], author=comment['author'], timestamp=comment['comment_date'],
                        text=comment['text'], parent_id=comment['parent_id'])
        if comment.get('children'):
            i += comments_filter(comment['children'])
    return mark_safe(res.format(i))
