from models.user import User


def get_controlled_user_ids(user):

    user_ids = []

    # নিজের ID
    user_ids.append(user.id)

    # সরাসরি controlled users
    children = User.query.filter_by(
        controller_id=user.id
    ).all()

    for child in children:

        user_ids.extend(
            get_controlled_user_ids(child)
        )

    return user_ids
