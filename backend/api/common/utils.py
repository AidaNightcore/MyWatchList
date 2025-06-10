def paginate(query, page=1, per_page=20):
    return query.paginate(page=page, per_page=per_page, error_out=False)

def pagination_dict(paginated_obj):
    return {
        'items': [item.to_dict() for item in paginated_obj.items],
        'total': paginated_obj.total,
        'pages': paginated_obj.pages,
        'current_page': paginated_obj.page
    }