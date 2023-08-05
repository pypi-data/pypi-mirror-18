from floraconcierge.client.types import Object


class Language(Object):
    """
    :type id: int
    :type iso: str
    :type name: str
    """

    def __init__(self, *args, **kwargs):
        self.icon = None
        self.id = None
        self.iso = None
        self.locale = None
        self.name = None

        super(Language, self).__init__(*args, **kwargs)


class User(Object):
    """
    :type auth: Auth
    :type gender: str
    :type id: int
    :type name: str
    """

    def __init__(self, *args, **kwargs):
        self.app_id = None
        self.auth = None
        self.birthday = None
        self.city = None
        self.corporate_account_bank = None
        self.corporate_account_bik = None
        self.corporate_account_kor = None
        self.corporate_account_number = None
        self.corporate_address_org = None
        self.corporate_address_post = None
        self.corporate_director = None
        self.corporate_inn = None
        self.corporate_ogrn = None
        self.corporate_organisation = None
        self.corporate_type = None
        self.country = None
        self.date_registration = None
        self.discount = None
        self.email = None
        self.feed_news = None
        self.feed_sms = None
        self.flowers = None
        self.gender = None
        self.id = None
        self.ip = None
        self.is_corporate_user = None
        self.name = None
        self.phone = None
        self.phone_home = None
        self.phone_work = None
        self.timezone = None

        super(User, self).__init__(*args, **kwargs)


class Snippet(Object):
    """
    :type id: int
    """

    def __init__(self, *args, **kwargs):
        self.application_id = None
        self.content = None
        self.id = None
        self.uid = None

        super(Snippet, self).__init__(*args, **kwargs)


class Page(Object):
    """
    :type id: int
    :type slug: str
    """

    def __init__(self, *args, **kwargs):
        self.application_id = None
        self.category = None
        self.content = None
        self.date = None
        self.file_name = None
        self.id = None
        self.is_file = None
        self.order = None
        self.promo = None
        self.published = None
        self.slug = None
        self.title = None
        self.url = None

        super(Page, self).__init__(*args, **kwargs)


class Review(Object):
    """
    :type category: str
    :type gender: str
    :type id: int
    :type name: str
    """

    def __init__(self, *args, **kwargs):
        self.allow_partners = None
        self.answer = None
        self.app_id = None
        self.avatar_url = None
        self.category = None
        self.city_id = None
        self.comment = None
        self.comment_courier = None
        self.comment_florist = None
        self.comment_florist_good = None
        self.comment_flowers_quality = None
        self.comment_flowers_rating = None
        self.comment_manager = None
        self.comment_operator = None
        self.country_id = None
        self.created = None
        self.email = None
        self.external_url = None
        self.gender = None
        self.id = None
        self.left = None
        self.name = None
        self.order_city = None
        self.order_country = None
        self.order_date = None
        self.order_id = None
        self.phone = None
        self.photo = None
        self.presents = None
        self.product_id = None
        self.rating = None
        self.rating_courier = None
        self.rating_florist = None
        self.rating_flowers = None
        self.rating_manager = None
        self.rating_operator = None
        self.rating_total = None
        self.right = None
        self.status = None
        self.urls = None
        self.user_id = None

        super(Review, self).__init__(*args, **kwargs)


class Calendar(Object):
    """
    :type id: int
    """

    def __init__(self, *args, **kwargs):
        self.country = None
        self.country_id = None
        self.date_end = None
        self.date_start = None
        self.every_year = None
        self.id = None
        self.title = None

        super(Calendar, self).__init__(*args, **kwargs)


class Inflect(Object):
    """
    :type id: int
    """

    def __init__(self, *args, **kwargs):
        self.fromloc = None
        self.id = None
        self.inflect1 = None
        self.inflect2 = None
        self.inflect3 = None
        self.inflect4 = None
        self.inflect5 = None
        self.inflect6 = None
        self.original = None
        self.toloc = None
        self.whereloc = None

        super(Inflect, self).__init__(*args, **kwargs)
