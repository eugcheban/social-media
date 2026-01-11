import pytest
from django.contrib.contenttypes.models import ContentType

from account.models import Account
from follow.models import Follow


@pytest.mark.django_db
def test_follow_links_generic_target(account_fixture, account_fixture_2):
	follower = account_fixture
	followee = account_fixture_2
	content_type = ContentType.objects.get_for_model(Account)

	follow = Follow.objects.create(
		user=follower,
		content_type=content_type,
		object_id=followee.id,
	)

	assert follow.target == followee
	assert follow.created_at is not None
