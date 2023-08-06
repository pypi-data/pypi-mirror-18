# import pytest
# pytest.mark
#
# k = 0
#
# class BaseTest:
#     c=None
#     @pytest.fixture(scope='class')
#     def page(self):
#         print('get page')
#         global k
#         k+=1
#         return self.c
#
#     @pytest.fixture(scope='class')
#     def g(self, page):
#         return page + 1
#
#     def test_c(self, page, g):
#         assert 1 == page
#         assert 2 == g
#
#     def test_d(self, page):
#         print(k)
#
#
# class TestA(BaseTest):
#     c=1
#
#
# class TestB(BaseTest):
#     c=2
#
#     def test_c(self, page, g):
#         assert 2==page
#         assert g==3
#
#     def test_r(self, g):
#         print(g)
#
#     def test_b(self, page):
#         print(k)
#         assert 0
#
#
#
# a = 1+5
#
# def test_a():
#     print(1)
#
#     assert a==3
