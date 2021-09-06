from matching.person import Person


class TestPerson:
    def test_to_dict_depth_zero(self, base_data):
        expected_values = base_data.values()
        assert set(Person(**base_data).to_dict(depth=0).values()) == set(
            expected_values
        )

    def test_to_dict_depth_one(self, base_data):
        test_person = Person(**base_data)
        test_person.connections.extend([Person(**base_data) for _ in range(3)])
        mentor_as_dict = test_person.to_dict()
        assert "match 1 email" in mentor_as_dict.keys()
