from accounts.test.test_setup import TestSetUp

class TestView(TestSetUp):

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        """
        # pdb is a python debugger with out exiting the program
        import pdb
        pdb.set_trace()"""
        self.assertEqual(res.status_code, 400)

    def test_user_can_register_correctly(self):
        res = self.client.post(
            self.register_url, 
            self.user_data, 
            format="json"
        )
        """import pdb
        pdb.set_trace()"""
        self.assertEqual(self.user_data['password'],self.user_data['password2'])
        self.assertEqual(res.data['Done']['email'], self.user_data['email'])
        self.assertEqual(res.data['Done']['username'], self.user_data['username'])

        self.assertEqual(res.status_code, 201)
    
    # def test_user_cannot_login_with_inactive_account(self):
    #     self.client.post(self.register_url, self.user_data, format="json")
    #     res = self.client.post(self.login_url, self.user_data, format="json")
    #     self.assertEqual(res.status_code, 200)
    
    # # def test_user_can_login_with_active_account(self):
    # #     user_data = self.user_data['is_active'] = True
    # #     self.client.post(self.register_url, user_data, format="json")
    # #     res = self.client.post(self.login_url, user_data, format='json')
    # #     self.assertEqual(res.status_code, 200)
