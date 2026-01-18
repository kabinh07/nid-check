import pandas as pd
import numpy as np
import os
from difflib import SequenceMatcher
import re
from datetime import datetime
import unicodedata

class ResultsEvaluator:
    """Evaluate NID data entry results against ground truth"""
    
    def __init__(self, person1_csv, person2_csv, ground_truth_csv):
        """
        Initialize evaluator with result files and ground truth
        
        Args:
            person1_csv: Path to person 1 results
            person2_csv: Path to person 2 results
            ground_truth_csv: Path to ground truth data (nid-data-140126.csv)
        """
        self.person1_results = pd.read_csv(person1_csv) if os.path.exists(person1_csv) else pd.DataFrame()
        self.person2_results = pd.read_csv(person2_csv) if os.path.exists(person2_csv) else pd.DataFrame()
        self.ground_truth = pd.read_csv(ground_truth_csv, sep='\t')
        
    def merge_results(self):
        """Merge person 1 and person 2 results"""
        merged = pd.concat([self.person1_results, self.person2_results], ignore_index=True)
        return merged
    
    def normalize_text(self, text_value):
        """
        Normalize text using Unicode NFC and strip whitespace
        Handles different Unicode representations of the same characters
        Converts Devanagari script to Bengali script
        Removes extra diacritical marks and viramas
        Removes problematic characters (Devanagari danda, etc.)
        """
        if pd.isna(text_value):
            return ""
        
        text_str = str(text_value).strip()
        # Apply NFC normalization
        text_str = unicodedata.normalize('NFC', text_str)
        
        # Remove Devanagari Danda and replace with space/period
        text_str = text_str.replace('\u0964', '.')  # Devanagari Danda -> period
        text_str = text_str.replace('\u0965', '.')  # Devanagari Double Danda -> period
        
        # Convert Devanagari to Bengali if present
        text_str = self._devanagari_to_bengali(text_str)
        
        # Remove extra/misplaced viramas (halant characters)
        text_str = self._remove_invalid_viramas(text_str)
        
        # Clean up multiple spaces
        text_str = ' '.join(text_str.split())
        
        return text_str
    
    def _remove_invalid_viramas(self, text):
        """
        Remove viramas (halant) that appear in invalid positions
        Bengali virama: U+09CD
        A virama is invalid if it appears after a vowel matra or at the end
        """
        virama = '\u09CD'
        vowel_matras = {
            '\u09BE',  # া (AA matra)
            '\u09BF',  # ি (I matra)
            '\u09C0',  # ী (II matra)
            '\u09C1',  # ু (U matra)
            '\u09C2',  # ূ (UU matra)
            '\u09C7',  # ে (E matra)
            '\u09C8',  # ৈ (AI matra)
            '\u09CB',  # ো (O matra)
            '\u09CC',  # ৌ (AU matra)
        }
        
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            
            if char == virama:
                # Check if this virama is invalid
                # It's invalid if previous character is a vowel matra or if it's at the start
                if i == 0 or text[i-1] in vowel_matras:
                    # Skip this invalid virama
                    i += 1
                    continue
            
            result.append(char)
            i += 1
        
        return ''.join(result)
    
    def _devanagari_to_bengali(self, text):
        """
        Convert Devanagari script characters to Bengali equivalents
        This handles cases where Hindi/Devanagari was typed instead of Bengali
        """
        # Mapping of Devanagari to Bengali Unicode characters
        # Devanagari Unicode: 0900-097F, Bengali Unicode: 0980-09FF
        devanagari_to_bengali = {
            # Consonants
            '\u0915': '\u0995',  # क -> ক
            '\u0916': '\u0996',  # ख -> খ
            '\u0917': '\u0997',  # ग -> গ
            '\u0918': '\u0998',  # घ -> ঘ
            '\u0919': '\u0999',  # ङ -> ঙ
            '\u091A': '\u099A',  # च -> চ
            '\u091B': '\u099B',  # छ -> ছ
            '\u091C': '\u099C',  # ज -> জ
            '\u091D': '\u099D',  # झ -> ঝ
            '\u091E': '\u099E',  # ञ -> ঞ
            '\u091F': '\u09A1',  # ट -> ট
            '\u0920': '\u09A2',  # ठ -> ঠ
            '\u0921': '\u09A3',  # ड -> ড
            '\u0922': '\u09A4',  # ढ -> ঢ
            '\u0923': '\u09A3',  # ण -> ণ
            '\u0924': '\u09A4',  # त -> ত
            '\u0925': '\u09A5',  # थ -> থ
            '\u0926': '\u09A6',  # द -> দ
            '\u0927': '\u09A7',  # ध -> ধ
            '\u0928': '\u09A8',  # न -> ন
            '\u092A': '\u09AA',  # प -> প
            '\u092B': '\u09AB',  # फ -> ফ
            '\u092C': '\u09AC',  # ब -> ব
            '\u092D': '\u09AD',  # भ -> ভ
            '\u092E': '\u09AE',  # म -> ম
            '\u092F': '\u09AF',  # य -> য
            '\u0930': '\u09B0',  # र -> র
            '\u0932': '\u09B2',  # ल -> ল
            '\u0935': '\u09B5',  # व -> ব
            '\u0936': '\u09B6',  # श -> শ
            '\u0937': '\u09B7',  # ष -> ষ
            '\u0938': '\u09B8',  # स -> স
            '\u0939': '\u09B9',  # ह -> হ
            # Vowels (independent forms)
            '\u0905': '\u0985',  # अ -> অ
            '\u0906': '\u0986',  # आ -> আ
            '\u0907': '\u0987',  # इ -> ই
            '\u0908': '\u0988',  # ई -> ঈ
            '\u0909': '\u0989',  # उ -> উ
            '\u090A': '\u098A',  # ऊ -> ঊ
            '\u090F': '\u098F',  # ए -> এ
            '\u0910': '\u0990',  # ऐ -> ৈ
            '\u0913': '\u0993',  # ओ -> ও
            '\u0914': '\u0994',  # औ -> ৌ
            # Vowel signs (matras/diacritics)
            '\u093E': '\u09BE',  # ा -> া (AA matra)
            '\u093F': '\u09BF',  # ि -> ি (I matra)
            '\u0940': '\u09C0',  # ी -> ী (II matra)
            '\u0941': '\u09C1',  # ु -> ু (U matra)
            '\u0942': '\u09C2',  # ू -> ূ (UU matra)
            '\u0947': '\u09C7',  # े -> ে (E matra)
            '\u0948': '\u09C8',  # ै -> ৈ (AI matra)
            '\u094B': '\u09CB',  # ो -> ো (O matra)
            '\u094C': '\u09CC',  # ौ -> ৌ (AU matra)
            # Special characters
            '\u094D': '\u09CD',  # ् -> ্ (virama/halant)
            '\u0902': '\u0981',  # ं -> ঁ (anusvara)
            '\u0903': '\u0983',  # ः -> ঃ (visarga)
            '\u0900': '\u0980',  # ॐ -> ৐ (om)
        }
        
        result = []
        for char in text:
            result.append(devanagari_to_bengali.get(char, char))
        return ''.join(result)
    
    def normalize_dob(self, dob_value):
        """
        Normalize DOB to YYYY-MM-DD format
        Handles: YYYY-MM-DD, YYYY/MM/DD, YYYYMMDD, etc.
        """
        if pd.isna(dob_value):
            return ""
        
        dob_str = str(dob_value).strip()
        
        # If already in YYYY-MM-DD format
        if re.match(r'^\d{4}-\d{2}-\d{2}$', dob_str):
            return dob_str
        
        # Replace common separators with dash
        dob_normalized = dob_str.replace('/', '-').replace(' ', '-')
        
        # Remove extra dashes and spaces
        dob_normalized = re.sub(r'-+', '-', dob_normalized).strip('-')
        
        # Try to parse and reformat
        for fmt in ['%Y-%m-%d', '%Y%m%d', '%d-%m-%Y', '%d/%m/%Y']:
            try:
                parsed = datetime.strptime(dob_normalized.replace('-', ''), fmt.replace('-', '').replace('/', ''))
                return parsed.strftime('%Y-%m-%d')
            except:
                continue
        
        return dob_str
    
    def normalize_nid(self, nid_value):
        """
        Normalize NID to integer (as string)
        Removes decimals, spaces, etc.
        """
        if pd.isna(nid_value):
            return ""
        
        nid_str = str(nid_value).strip()
        
        # Remove decimal point if present (e.g., 6032068741.0 -> 6032068741)
        if '.' in nid_str:
            nid_str = nid_str.split('.')[0]
        
        # Remove any non-digit characters
        nid_str = re.sub(r'\D', '', nid_str)
        
        return nid_str
    
    def extract_image_id(self, front_image_path):
        """Extract image ID from front_image path"""
        if isinstance(front_image_path, str) and '/' in front_image_path:
            return front_image_path.split('/')[-1].replace('.jpg', '')
        return str(front_image_path).replace('.jpg', '')
    
    def character_error_rate(self, actual, predicted):
        """Calculate Character Error Rate (CER)"""
        if pd.isna(actual) or pd.isna(predicted):
            return 100.0
        
        actual_str = self.normalize_text(actual).lower()
        predicted_str = self.normalize_text(predicted).lower()
        
        if len(actual_str) == 0:
            return 0.0 if len(predicted_str) == 0 else 100.0
        
        # Levenshtein distance at character level
        matcher = SequenceMatcher(None, actual_str, predicted_str)
        ratio = matcher.ratio()
        cer = (1 - ratio) * 100
        return round(cer, 2)
    
    def word_error_rate(self, actual, predicted):
        """Calculate Word Error Rate (WER)"""
        if pd.isna(actual) or pd.isna(predicted):
            return 100.0
        
        actual_words = self.normalize_text(actual).lower().split()
        predicted_words = self.normalize_text(predicted).lower().split()
        
        if len(actual_words) == 0:
            return 0.0 if len(predicted_words) == 0 else 100.0
        
        # Calculate word-level accuracy
        matcher = SequenceMatcher(None, actual_words, predicted_words)
        ratio = matcher.ratio()
        wer = (1 - ratio) * 100
        return round(wer, 2)
    
    def field_accuracy(self, actual, predicted):
        """Calculate field-level accuracy (exact match or high similarity)"""
        if pd.isna(actual) and pd.isna(predicted):
            return 100.0
        if pd.isna(actual) or pd.isna(predicted):
            return 0.0
        
        actual_str = self.normalize_text(actual).lower()
        predicted_str = self.normalize_text(predicted).lower()
        
        if actual_str == predicted_str:
            return 100.0
        
        # Calculate similarity ratio
        matcher = SequenceMatcher(None, actual_str, predicted_str)
        return round(matcher.ratio() * 100, 2)
    
    def evaluate(self):
        """Evaluate all results and generate comparison CSV"""
        # Merge results from both persons
        merged_results = self.merge_results()
        
        # Create image_id column in ground truth from both front and back images
        self.ground_truth['image_id'] = self.ground_truth['front_image'].apply(self.extract_image_id)
        # Add fallback from back_image if front_image is missing
        self.ground_truth['image_id_back'] = self.ground_truth['back_image'].apply(self.extract_image_id)
        
        # Create evaluation dataframe
        evaluation_data = []
        matched_count = 0
        no_match_count = 0
        
        for idx, row in merged_results.iterrows():
            # Extract ground truth values (from entered data - persons 1 and 2)
            gt_english = row.get('english_name', '')
            gt_bangla = row.get('bangla_name', '')
            gt_father = row.get('father_spouse_name', '')
            gt_mother = row.get('mother_name', '')
            gt_dob = row.get('dob', '')
            gt_nid = row.get('nid_no', '')
            gt_address = row.get('plain_address', '')
            image_id = row.get('image_id', '')
            
            # Try to find matching prediction (from nid-data-140126.csv) by:
            # 1. PRIORITY: Match by image_id (front or back) - most reliable
            # 2. FALLBACK: Match by NID number only if image_id is missing or not found
            pred_row = None
            match_method = None
            
            # Try matching by image_id (from front_image) - PRIMARY METHOD
            if image_id:
                pred_matches = self.ground_truth[self.ground_truth['image_id'].astype(str) == str(image_id)]
                if not pred_matches.empty:
                    pred_row = pred_matches.iloc[0]
                    matched_count += 1
                    match_method = 'front_image_id'
            
            # Try matching by back_image if front didn't match - SECONDARY METHOD
            if pred_row is None and image_id:
                pred_matches = self.ground_truth[self.ground_truth['image_id_back'].astype(str) == str(image_id)]
                if not pred_matches.empty:
                    pred_row = pred_matches.iloc[0]
                    matched_count += 1
                    match_method = 'back_image_id'
            
            # ONLY use NID matching if image_id is missing (no image data was submitted)
            # This prevents matching to wrong records when multiple NIDs exist
            if pred_row is None and (not image_id or str(image_id).strip() == ''):
                if gt_nid:
                    pred_matches = self.ground_truth[
                        self.ground_truth['nid_no'].astype(str).str.replace('.0', '') == str(gt_nid).replace('.0', '')
                    ]
                    if not pred_matches.empty:
                        pred_row = pred_matches.iloc[0]
                        matched_count += 1
                        match_method = 'nid_number'
            
            if pred_row is None:
                # If no match found, skip this record
                no_match_count += 1
                continue
            
            # Extract predicted (Polygon OCR from nid-data-140126.csv) values
            pred_english = pred_row.get('name_english', '')
            pred_bangla = pred_row.get('name_bangla', '')
            pred_father = pred_row.get('father_name', '')
            pred_mother = pred_row.get('mother_name', '')
            pred_dob = pred_row.get('dob', '')
            pred_nid = pred_row.get('nid_no', '')
            pred_address = pred_row.get('address', '')
            pred_doc_date = pred_row.get('doc_date', '')
            
            # Normalize DOB and NID for comparison
            gt_dob_norm = self.normalize_dob(gt_dob)
            pred_dob_norm = self.normalize_dob(pred_dob)
            gt_nid_norm = self.normalize_nid(gt_nid)
            pred_nid_norm = self.normalize_nid(pred_nid)
            

            # Calculate metrics for each field
            english_acc = self.field_accuracy(gt_english, pred_english)
            english_cer = self.character_error_rate(gt_english, pred_english)
            english_wer = self.word_error_rate(gt_english, pred_english)
            
            bangla_acc = self.field_accuracy(gt_bangla, pred_bangla)
            bangla_cer = self.character_error_rate(gt_bangla, pred_bangla)
            bangla_wer = self.word_error_rate(gt_bangla, pred_bangla)
            
            father_acc = self.field_accuracy(gt_father, pred_father)
            father_cer = self.character_error_rate(gt_father, pred_father)
            father_wer = self.word_error_rate(gt_father, pred_father)
            
            mother_acc = self.field_accuracy(gt_mother, pred_mother)
            mother_cer = self.character_error_rate(gt_mother, pred_mother)
            mother_wer = self.word_error_rate(gt_mother, pred_mother)
            
            # Use normalized DOB for comparison
            dob_acc = self.field_accuracy(gt_dob_norm, pred_dob_norm)
            dob_cer = self.character_error_rate(gt_dob_norm, pred_dob_norm)
            dob_wer = self.word_error_rate(gt_dob_norm, pred_dob_norm)
            
            # Use normalized NID for comparison
            nid_acc = self.field_accuracy(gt_nid_norm, pred_nid_norm)
            nid_cer = self.character_error_rate(gt_nid_norm, pred_nid_norm)
            nid_wer = self.word_error_rate(gt_nid_norm, pred_nid_norm)
            
            # Use address for comparison (without prefix)
            address_acc = self.field_accuracy(gt_address, pred_address)
            address_cer = self.character_error_rate(gt_address, pred_address)
            address_wer = self.word_error_rate(gt_address, pred_address)
            
            # Overall accuracy (average of all fields)
            overall_acc = np.mean([english_acc, bangla_acc, father_acc, mother_acc, dob_acc, nid_acc, address_acc])
            overall_cer = np.mean([english_cer, bangla_cer, father_cer, mother_cer, dob_cer, nid_cer, address_cer])
            overall_wer = np.mean([english_wer, bangla_wer, father_wer, mother_wer, dob_wer, nid_wer, address_wer])
            
            eval_row = {
                'image_id': image_id,
                
                # Ground Truth (Entered) Values
                'actual_english_name': gt_english,
                'actual_bangla_name': gt_bangla,
                'actual_father_spouse': gt_father,
                'actual_mother': gt_mother,
                'actual_dob': gt_dob_norm,  # Use normalized format
                'actual_nid_no': gt_nid_norm,  # Use normalized format
                'actual_address': gt_address,
                
                # Predicted (Polygon OCR from nid-data-140126.csv) Values
                'predicted_english_name': pred_english,
                'predicted_bangla_name': pred_bangla,
                'predicted_father_spouse': pred_father,
                'predicted_mother': pred_mother,
                'predicted_dob': pred_dob_norm,  # Use normalized format
                'predicted_nid_no': pred_nid_norm,  # Use normalized format
                'predicted_address': pred_address,
                'predicted_doc_date': pred_doc_date,
                
                # English Name Metrics
                'english_name_accuracy': english_acc,
                'english_name_cer': english_cer,
                'english_name_wer': english_wer,
                
                # Bangla Name Metrics
                'bangla_name_accuracy': bangla_acc,
                'bangla_name_cer': bangla_cer,
                'bangla_name_wer': bangla_wer,
                
                # Father/Spouse Metrics
                'father_spouse_accuracy': father_acc,
                'father_spouse_cer': father_cer,
                'father_spouse_wer': father_wer,
                
                # Mother Metrics
                'mother_accuracy': mother_acc,
                'mother_cer': mother_cer,
                'mother_wer': mother_wer,
                
                # DOB Metrics
                'dob_accuracy': dob_acc,
                'dob_cer': dob_cer,
                'dob_wer': dob_wer,
                
                # NID Metrics
                'nid_no_accuracy': nid_acc,
                'nid_no_cer': nid_cer,
                'nid_no_wer': nid_wer,
                
                # Address Metrics
                'address_accuracy': address_acc,
                'address_cer': address_cer,
                'address_wer': address_wer,
                
                # Overall Metrics
                'overall_accuracy': round(overall_acc, 2),
                'overall_cer': round(overall_cer, 2),
                'overall_wer': round(overall_wer, 2),
            }
            
            evaluation_data.append(eval_row)
        
        return pd.DataFrame(evaluation_data)
    
    def generate_report(self, output_csv):
        """Generate evaluation report and save to CSV"""
        # Get merged results before evaluation to track statistics
        merged_results = self.merge_results()
        total_records = len(merged_results)
        
        evaluation_df = self.evaluate()
        
        if len(evaluation_df) == 0:
            print("\n" + "="*80)
            print("WARNING: No matching records found between entered data and ground truth!")
            print("="*80)
            print(f"\nRecord Matching Summary:")
            print(f"  Total entered records: {total_records}")
            print(f"  Matched with ground truth: 0")
            print(f"  No match found: {total_records}")
            print("\nPossible reasons:")
            print("  1. Image IDs don't match between datasets")
            print("  2. NID numbers are different or missing")
            print("  3. No data has been entered yet")
            print("\nCreating empty evaluation file...")
            evaluation_df.to_csv(output_csv, index=False)
            return evaluation_df
        
        matched_records = len(evaluation_df)
        unmatched_records = total_records - matched_records
        match_rate = (matched_records / total_records * 100) if total_records > 0 else 0
        
        evaluation_df.to_csv(output_csv, index=False)
        
        # Print summary statistics
        print("\n" + "="*80)
        print("EVALUATION REPORT SUMMARY")
        print("="*80)
        print(f"Record Matching Summary:")
        print(f"  Total entered records: {total_records}")
        print(f"  Matched with ground truth: {matched_records}")
        print(f"  No match found: {unmatched_records}")
        print(f"  Match rate: {match_rate:.2f}%")
        print(f"\nTotal records evaluated: {matched_records}")
        print(f"\nOverall Statistics:")
        print(f"  Average Accuracy: {evaluation_df['overall_accuracy'].mean():.2f}%")
        print(f"  Average CER: {evaluation_df['overall_cer'].mean():.2f}%")
        print(f"  Average WER: {evaluation_df['overall_wer'].mean():.2f}%")
        
        print(f"\nPer-Field Statistics:")
        fields = ['english_name', 'bangla_name', 'father_spouse', 'mother', 'dob', 'nid_no', 'address']
        for field in fields:
            acc_col = f'{field}_accuracy'
            cer_col = f'{field}_cer'
            wer_col = f'{field}_wer'
            print(f"\n  {field.upper()}:")
            print(f"    Accuracy: {evaluation_df[acc_col].mean():.2f}%")
            print(f"    CER: {evaluation_df[cer_col].mean():.2f}%")
            print(f"    WER: {evaluation_df[wer_col].mean():.2f}%")
        
        print(f"\nEvaluation report saved to: {output_csv}")
        print("="*80 + "\n")
        
        return evaluation_df


def main():
    """Main function to run evaluation"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define file paths
    person1_results = os.path.join(project_root, "data", "nid-data-entry-results-person1.csv")
    person2_results = os.path.join(project_root, "data", "nid-data-entry-results-person2.csv")
    ground_truth = os.path.join(project_root, "data", "nid-data-140126.csv")
    output_csv = os.path.join(project_root, "data", "evaluation_results.csv")
    
    # Run evaluation
    evaluator = ResultsEvaluator(person1_results, person2_results, ground_truth)
    evaluator.generate_report(output_csv)


if __name__ == "__main__":
    main()
