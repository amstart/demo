from .base import BlockObjectsTests

class CreateObjectTest(BlockObjectsTests):
    def setUp(self):
        self.login()
        self.response = self.client.post(self.URL_create(), self.post_params[0])
        self.latest_model = self.model.objects.all().latest()
        self.latest_model_id = self.latest_model.pk

    def test_redirecting_works(self):
        self.assertRedirects(self.response, self.URL_detail(self.latest_model_id))

    def test_detail_view(self):
        self.client.logout()
        response = self.client.get(self.URL_detail(pk = self.latest_model_id))
        self.assertEqual(response.status_code, 200)
        if self.is_premise:
            for key, value in self.post_params[0].items():
                self.assertContains(response, value)
                self.assertContains(response, "class=\"" + key + "\"")
        else:
            object = self.get_object(pk = self.latest_model_id)
            for key, value in self.post_params[0].items():
                if key == 'aim':
                    self.assertContains(response, object.choice_headings[object.aim-1])
                else:
                    self.assertContains(response, str(getattr(object, key)))

class FailCreateObjectTest(BlockObjectsTests):
    def test_redirect_to_form_again(self):
        self.login()
        response = self.client.post(self.URL_create(), self.no_post_params[0])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blockobjects/create_object.html')
