import unittest, os, sys, json

# Mock streamlit before importing app
import streamlit as st
st.session_state = {"lang": "es"}
st.secrets = {}

sys.modules["streamlit"] = st

import app

class TestCleanMashi(unittest.TestCase):
    def test_spanish_mashi_to_amigo(self):
        r = app._clean_mashi("Hola, mashi!", "es")
        self.assertIn("amigo", r)
        self.assertNotIn("mashi", r)

    def test_spanish_mashi_sugiere_to_recomiendo(self):
        r = app._clean_mashi("Mashi sugiere invertir", "es")
        self.assertIn("Recomiendo", r)

    def test_english_mashi_to_friend(self):
        r = app._clean_mashi("Hello, mashi!", "en")
        self.assertIn("friend", r)
        self.assertNotIn("mashi", r)

    def test_english_mashi_suggests(self):
        r = app._clean_mashi("Mashi suggests", "en")
        self.assertIn("I suggest", r)

    def test_kichwa_preserves_mashi(self):
        r = app._clean_mashi("Allianllachu, mashi!", "qw")
        self.assertIn("mashi", r)

class TestL(unittest.TestCase):
    def test_spanish_default(self):
        app.st.session_state = {"lang": "es"}
        self.assertEqual(app._L("Hola","Hello","Alli"), "Hola")

    def test_english(self):
        app.st.session_state = {"lang": "en"}
        self.assertEqual(app._L("Hola","Hello","Alli"), "Hello")

    def test_kichwa(self):
        app.st.session_state = {"lang": "qw"}
        self.assertEqual(app._L("Hola","Hello","Alli"), "Alli")

    def test_kichwa_fallback(self):
        app.st.session_state = {"lang": "qw"}
        self.assertEqual(app._L("Hola","Hello"), "Hola")

class TestGetFullDataset(unittest.TestCase):
    def test_returns_list(self):
        app.st.session_state = {"lang": "es", "new_entrepreneurs": []}
        data = app.get_full_dataset()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_communities_have_required_keys(self):
        app.st.session_state = {"lang": "es", "new_entrepreneurs": []}
        data = app.get_full_dataset()
        required = {"id","name","location","sector","products","reviews"}
        for c in data:
            with self.subTest(name=c["name"]):
                self.assertTrue(required.issubset(c.keys()),
                    f"Missing keys: {required - c.keys()}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
