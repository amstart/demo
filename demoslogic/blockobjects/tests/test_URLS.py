from .base import BlockObjectsTests

class URLTest(BlockObjectsTests):
    def test_index_view(self):
        response = self.client.get(self.URL_index())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blockobjects/index.html')

    def test_detail_view_without_empty_choice(self):
        response = self.client.get(self.URL_detail())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blockobjects/detail.html')
        self.assertNotContains(response, '---')
