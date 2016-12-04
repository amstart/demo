from .base import BlockObjectsTests
from demoslogic.blockobjects.templatetags.blockobjects_tags import print_premise

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
        object = self.get_object(pk = self.latest_model_id)
        if self.is_premise:
            self.assertContains(response, object.sentence)
        else:
            self.assertContains(response, object.aim_heading)
            self.assertContains(response, object.premise1_thesis)
            self.assertContains(response, object.premise2_thesis)
            for key, value in self.create_params[0].items():
                if key.find('_id') > -1:
                    self.assertContains(response, print_premise(getattr(object, key[0:-3])))

class FailCreateObjectTest(BlockObjectsTests):
    def test_redirect_to_form_again(self):
        self.login()
        for no_post_param in self.no_post_params:
            response = self.client.post(self.URL_create(), no_post_param)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blockobjects/create_object.html')
