import copy
import unittest
from core import analyse,DEMO

class MarkingTests(unittest.TestCase):
    def test_known_scores(self):
        r=analyse(DEMO)
        self.assertEqual([s['score'] for s in r['rows']],[5,3,2,1,4])
        self.assertEqual(r['summary'][1][1],'60.0%')
        self.assertEqual(r['summary'][2][1],'60.0%')
        self.assertEqual(r['items'][4]['blank'],1)
        self.assertEqual(r['items'][0]['correct'],3)

    def test_duplicate_ids_rejected(self):
        d=copy.deepcopy(DEMO);d['responses_csv']+='demo001,Duplicate,B,A,D,C,B\n'
        with self.assertRaisesRegex(ValueError,'Duplicate'):analyse(d)

    def test_missing_column_rejected(self):
        d=copy.deepcopy(DEMO);d['answer_key']['Q6']='C'
        with self.assertRaisesRegex(ValueError,'Missing'):analyse(d)

    def test_invalid_answer_rejected(self):
        d=copy.deepcopy(DEMO);d['responses_csv']=d['responses_csv'].replace('B,A,D,C,B','Z,A,D,C,B')
        with self.assertRaisesRegex(ValueError,'Invalid'):analyse(d)

    def test_bom_and_quoted_name(self):
        d={'answer_key':{'Q1':'A'},'responses_csv':'\ufeffstudent_id,name,Q1\nS1,"Doe, Jane", a \n'}
        r=analyse(d);self.assertEqual(r['rows'][0]['name'],'Doe, Jane');self.assertEqual(r['rows'][0]['score'],1)

    def test_pass_threshold_uses_unrounded_score(self):
        d={'answer_key':{'Q1':'A','Q2':'B','Q3':'C'},'pass_mark':66.67,'responses_csv':'student_id,name,Q1,Q2,Q3\nS1,Demo,A,B,A\n'}
        r=analyse(d)['rows'][0];self.assertEqual(r['percentage'],66.67);self.assertEqual(r['result'],'Below pass mark')

    def test_empty_responses_rejected(self):
        d=copy.deepcopy(DEMO);d['responses_csv']='student_id,name,Q1,Q2,Q3,Q4,Q5\n'
        with self.assertRaises(ValueError):analyse(d)

    def test_extra_cell_rejected(self):
        d=copy.deepcopy(DEMO);d['responses_csv']+='S8,Demo,A,A,A,A,A,EXTRA\n'
        with self.assertRaisesRegex(ValueError,'Malformed'):analyse(d)

if __name__=='__main__':unittest.main()
