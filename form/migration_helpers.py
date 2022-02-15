import uuid
def create_uuid(apps, schema_editor):
    chat = apps.get_model('form', 'Chat')
    for chat_item in chat.objects.all():
        chat_item.slug = uuid.uuid4()
        chat_item.save()

# copy paste this
