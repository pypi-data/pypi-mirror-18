from flask_restplus import Namespace, Resource, fields

api = Namespace('calendar', description='Calendar')

calendar = api.model('Calendar', {
    'id': fields.String(required=True, description='The Event Identifier'),
    'name': fields.String(required=True, description='The Event Name'),
    'date': fields.String(required=True, description='The Event Date'),
})

EVENTS = [
    {'id': '1', 'name': 'Manger' , 'date':'3 Juillet'},
]


@api.route('/')
class CalendarList(Resource):
    @api.doc('list_event')
    @api.marshal_list_with(calendar)
    def get(self):
        '''List all event'''
        return EVENTS


@api.route('/<id>')
@api.param('id', 'The Event Identifier')
@api.response(404, 'Event not found')
class CalendarEvent(Resource):
    @api.doc('get_event')
    @api.marshal_with(calendar)
    def get(self, id):
        '''Fetch a event given its identifier'''
        for event in EVENTS:
            if event['id'] == id:
                return event
        api.abort(404)
