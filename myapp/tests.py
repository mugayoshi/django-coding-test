from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from myapp.models import Channel, Content
from myapp.services.channel_rating_service import calculate_channel_ratings

class ChannelListViewTestCase(TestCase):
    url_name = 'channel list'
    def setUp(self):
        self.client = APIClient()

        self.content1 = Content.objects.create(
            title="Content 1", 
            metadata={"description": "First content"},
            rating=7.5
        )
        self.content2 = Content.objects.create(
            title="Content 2", 
            metadata={"description": "Second content"},
            rating=8.0
        )
        self.content3 = Content.objects.create(
            title="Content 3", 
            metadata={"description": "Third content"},
            rating=6.5
        )
        self.content4 = Content.objects.create(
            title="Content 4", 
            metadata={"description": "Fourth content"},
            rating=9.0
        )
        self.content5 = Content.objects.create(
            title="Content 5", 
            metadata={"description": "Fifth content"},
            rating=7.0
        )

        self.channel1 = Channel.objects.create(
            title="Channel 1", 
            language="English"
        )
        self.channel1.contents.add(self.content1, self.content2)

        self.channel2 = Channel.objects.create(
            title="Channel 2", 
            language="Spanish"
        )
        self.channel2.contents.add(self.content3, self.content4, self.content5)

        self.parent_channel = Channel.objects.create(
            title="Parent Channel", 
            language="French"
        )

        self.subchannel1 = Channel.objects.create(
            title="Subchannel 1", 
            language="German",
            parent_channel=self.parent_channel
        )
        self.subchannel1.contents.add(self.content1, self.content2)

        self.subchannel2 = Channel.objects.create(
            title="Subchannel 2", 
            language="Italian",
            parent_channel=self.parent_channel
        )
        self.subchannel2.contents.add(self.content3, self.content4, self.content5)

    def test_channel_list_view(self):
        """
        Test that the ChannelListView returns only top-level channels
        """
        url = reverse(self.url_name)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 3)
        
        channel_titles = [channel['title'] for channel in response.data]
        self.assertIn("Channel 1", channel_titles)
        self.assertIn("Channel 2", channel_titles)
        self.assertIn("Parent Channel", channel_titles)
        
        for channel in response.data:
            if channel['title'] == "Channel 1":
                self.assertEqual(len(channel['contents']), 2)
            elif channel['title'] == "Parent Channel":
                self.assertEqual(len(channel['contents']), 0)

    def test_channel_serializer_content(self):
        """
        Test that the serializer includes the correct content information
        """
        url = reverse(self.url_name)
        response = self.client.get(url)
        
        for channel in response.data:
            if channel['title'] == "Channel 1":
                contents = channel['contents']
                self.assertEqual(len(contents), 2)
                content_titles = [content['title'] for content in contents]
                self.assertIn("Content 1", content_titles)
                self.assertIn("Content 2", content_titles)

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