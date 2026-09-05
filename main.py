#!/usr/bin/env python3
"""
Main entry point for devtools utility collection.
Usage: python main.py <command> [args...]
"""
import sys
import importlib
import argparse
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

# Command to module/class mapping
COMMANDS = {
    # Automation
    'watch': ('automation.file_watcher', 'FileWatcher'),
    'build': ('automation.project_builder', 'ProjectBuilder'),
    
    # Core
    'encrypt': ('core.crypto_utils', 'CryptoUtils'),
    'decrypt': ('core.crypto_utils', 'CryptoUtils'),
    
    # Data Analysis
    'analyze': ('data_analysis.universal_analyzer', 'UniversalAnalyzer'),
    'gen-data': ('data_analysis.data_preparer', 'DataPreparer'),
    'db-visual': ('data_analysis.database_visualizer', 'DatabaseVisualizer'),
    'inspect': ('data_analysis.project_inspector', 'ProjectInspector'),
    'excel': ('data_analysis.excel_processor', 'ExcelProcessor'),
    
    # Media
    'pdf': ('media.pdf_tool', 'PDFTool'),
    'contacts': ('media.contact_generator', 'ContactGenerator'),
    'audio': ('media.audio_synthesizer', 'AudioSynthesizer'),
    
    # Scripts
    'reset-db': ('scripts.db_reinitializer', 'DBReinitializer'),
    'mk-structure': ('scripts.structure_creator', 'StructureCreator'),
    'replace': ('scripts.string_replacer', 'StringReplacer'),
    'merge-text': ('scripts.text_merger', 'TextMerger'),
}


def run_command(cmd, args):
    """Import and run command with given args."""
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        print(f"Available: {', '.join(sorted(COMMANDS.keys()))}")
        return 1
    
    module_path, class_name = COMMANDS[cmd]
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)
    
    # Run as script
    if hasattr(module, 'main') and not args:
        module.main()
        return 0
    
    # Create instance and call method
    if cmd == 'merge-text':
        from scripts.text_merger import TextMerger
        TextMerger.merge(args[0]) if args else None
    elif cmd == 'watch':
        if len(args) >= 2:
            watcher = cls(args[0], args[1])
            watcher.run()
    elif cmd == 'build':
        builder = cls()
        builder.build_from_file(args[0], args[1] if len(args) > 1 else None)
    elif cmd == 'encrypt':
        cls.encrypt_file(args[0], args[1], args[2] if len(args) > 2 else None)
    elif cmd == 'decrypt':
        cls.decrypt_file(args[0], args[1], args[2] if len(args) > 2 else None)
    elif cmd == 'analyze':
        analyzer = cls()
        analyzer.load_data(args[0])
        if len(args) > 1:
            analyzer.set_config(outcome_var=args[1])
            print(analyzer.bivariate_analysis())
        analyzer.create_report()
    elif cmd == 'gen-data':
        from data_analysis.data_preparer import DataPreparer
        n = int(args[0]) if args else 100
        df = DataPreparer.generate_hookworm_data(n)
        DataPreparer.save_dataset(df, args[1] if len(args) > 1 else 'sample_data.csv')
    elif cmd == 'db-visual':
        cls.print_structure(args[0])
    elif cmd == 'inspect':
        cls.save_structure(args[0] if args else '.', args[1] if len(args) > 1 else 'structure.txt')
    elif cmd == 'excel':
        processor = cls()
        processor.load(args[0])
        data = processor.read_sheet()
        processor.save(data, args[1] if len(args) > 1 else 'processed.xlsx')
    elif cmd == 'pdf':
        tool = cls(args[0])
        tool.extract_text()
        if len(args) > 1:
            tool.speak_page(int(args[1]))
        else:
            for text in tool.text.values():
                tool.speak(text)
    elif cmd == 'contacts':
        generator = cls()
        if len(args) > 0 and args[0] == 'filter':
            generator.filter_no_name(args[1] if len(args) > 1 else 'contacts.vcf')
        else:
            count = int(args[0]) if args else 10000
            generator.generate(count=count)
    elif cmd == 'audio':
        from media.audio_synthesizer import AudioSynthesizer
        synth = cls()
        if args and args[0] == 'theme':
            synth.create_interstellar_theme()
        else:
            melody = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
            samples = []
            for note in melody:
                samples.extend(synth.generate_note(note, 0.3, 0.7))
            synth.save_wav(samples, "melody.wav")
            print("Generated: melody.wav")
    elif cmd == 'reset-db':
        cls.reset(args[0] if args else '.')
    elif cmd == 'mk-structure':
        cls.create_django_structure(args[0] if args else 'myproject')
    elif cmd == 'replace':
        cls.replace(args[0], args[1], args[2], args[3:] if len(args) > 3 else None)
    else:
        print(f"Command {cmd} not yet implemented")
        return 1
    
    return 0


def main():
    if len(sys.argv) < 2:
        print("DevTools - Private Utility Collection")
        print("\nUsage: python main.py <command> [args...]")
        print(f"\nCommands: {', '.join(sorted(COMMANDS.keys()))}")
        print("\nExamples:")
        print("  python main.py merge-text ./myproject")
        print("  python main.py watch ./src ./dist")
        print("  python main.py build metafile.txt")
        print("  python main.py analyze data.csv hemoglobin")
        print("  python main.py encrypt file.txt password")
        return 1
    
    cmd = sys.argv[1].replace('-', '_')
    args = sys.argv[2:]
    
    # Map hyphens to underscores
    for key in list(COMMANDS.keys()):
        if key.replace('-', '_') == cmd:
            return run_command(key, args)
    
    return run_command(cmd, args)


if __name__ == "__main__":
    sys.exit(main())
