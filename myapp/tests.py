from django.test import TestCase
from myapp.models import Channel, Content
from myapp.services.channel_rating_service import calculate_channel_ratings

class ChannelRatingServiceTests(TestCase):
    def setUp(self):
        channel1 = Channel.objects.create(
            title="channel1",
            language="English"
        )
        content1_1 = Content.objects.create(
            title="content1_1",
            rating=8.5
        )
        content1_2 = Content.objects.create(
            title="content1_2",
            rating=9.0
        )
        channel1.contents.add(content1_1, content1_2)

        channel2 = Channel.objects.create(
            title="channel2",
            language="English"
        )
        content2_1 = Content.objects.create(
            title="content2_1",
            rating=7.5
        )
        content2_2 = Content.objects.create(
            title="content2_2",
            rating=8.0
        )
        channel2.contents.add(content2_1, content2_2)

        # Channel with subchannels (should be excluded)
        parent_channel = Channel.objects.create(
            title="parent_channel",
            language="English"
        )
        
        # Create subchannels
        subchannel1 = Channel.objects.create(
            title="subchannel1",
            language="English",
            parent_channel=parent_channel
        )
        content_subchannel_1 = Content.objects.create(
            title="content_subchannel_1",
            rating=4
        )
        subchannel1.contents.add(content_subchannel_1)
        subchannel2 = Channel.objects.create(
            title="subchannel2",
            language="English",
            parent_channel=parent_channel
        )
        content_subchannel_2 = Content.objects.create(
            title="content_subchannel_2",
            rating=3
        )
        subchannel2.contents.add(content_subchannel_2)

        # Channel with no contents (should be excluded)
        Channel.objects.create(
            title="Empty Channel",
            language="English"
        )

    def test_calculate_channel_ratings(self):
        rated_channels = calculate_channel_ratings()

        self.assertEqual(len(rated_channels), 4, "Should only include channels with contents")

        self.assertEqual(rated_channels[0].title, "channel1")
        self.assertAlmostEqual(rated_channels[0].avg_rating, 8.75)

        self.assertEqual(rated_channels[1].title, "channel2")
        self.assertAlmostEqual(rated_channels[1].avg_rating, 7.75)

    def test_channel_ratings_order(self):
        rated_channels = calculate_channel_ratings()

        self.assertTrue(
            rated_channels[0].avg_rating > rated_channels[1].avg_rating, 
            "Channels should be sorted in descending order"
        )

    def test_empty_channel_exclusion(self):
        rated_channels = calculate_channel_ratings()

        channel_titles = [channel.title for channel in rated_channels]
        self.assertNotIn("Empty Channel", channel_titles)
    
    def test_parent_channel_with_subchannels(self):
        parent_channel = Channel.objects.get(title="parent_channel")
        
        self.assertTrue(parent_channel.subchannels.exists())
        self.assertFalse(parent_channel.contents.exists())

        rated_channels = calculate_channel_ratings()
        channel_titles = [channel.title for channel in rated_channels]
        self.assertNotIn("parent_channel", channel_titles)

        self.assertEqual(rated_channels[2].title, "subchannel1")
        self.assertEqual(rated_channels[2].avg_rating, 4)

        self.assertEqual(rated_channels[3].title, "subchannel2")
        self.assertEqual(rated_channels[3].avg_rating, 3)