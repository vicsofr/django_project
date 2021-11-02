def get_children(qs_child):
    res = []
    for comment in qs_child:
        c = {
            'id': comment.id,
            'text': comment.text,
            'comment_date': comment.comment_date.strftime('%d-%m-%Y %H:%m'),
            'author': comment.author_id,
            'is_child': comment.is_child,
            'parent_id': comment.get_parent
        }
        if comment.child_comment.exists:
            c['children'] = get_children(comment.child_comment.all())
        res.append(c)
    return res


def create_comment_tree(qs):
    res = []
    for comment in qs:
        c = {
            'id': comment.id,
            'text': comment.text,
            'comment_date': comment.comment_date.strftime('%Y-%m-%d %H:%m'),
            'author': comment.author_id,
            'is_child': comment.is_child,
            'parent_id': comment.get_parent
        }
        if comment.child_comment:
            c['children'] = get_children(comment.child_comment.all())
        if not comment.is_child:
            res.append(c)
    return res
