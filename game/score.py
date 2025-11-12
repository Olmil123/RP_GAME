from game.settings import MAX_RECORDS_NUMBER


class PlayerRecord:
    def __init__(self, name: str, mode: str, score: int):
        self.name = name
        self.mode = mode
        self.score = int(score)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PlayerRecord):
            return NotImplemented
        return self.score < other.score

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, PlayerRecord):
            return NotImplemented
        return self.score > other.score

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlayerRecord):
            return False
        return self.name == other.name and self.mode == other.mode

    def __str__(self) -> str:
        return f"{self.name} {self.mode} {self.score}"


class GameRecord:
    def __init__(self):
        self.records: list[PlayerRecord] = []

    def add_record(self, record: PlayerRecord):
        for i, existing in enumerate(self.records):
            if existing == record:
                self.records[i] = record
                break
        else:
            self.records.append(record)

    def prepare_records(self):
        self.records.sort(reverse=True)
        self.records = self.records[:MAX_RECORDS_NUMBER]


class ScoreHandler:

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.game_record = GameRecord()
        self.read()

    def read(self):
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split()
                    if len(parts) != 3:
                        continue
                    name, mode, score_str = parts
                    record = PlayerRecord(name, mode, int(score_str))
                    self.game_record.add_record(record)
        except FileNotFoundError:
            pass

    def save(self):
        self.game_record.prepare_records()
        with open(self.file_name, "w", encoding="utf-8") as f:
            for record in self.game_record.records:
                f.write(str(record) + "\n")

    def display(self):
        if not self.game_record.records:
            print("No scores yet")
            return
        print("\n=== High Scores ===")
        print(f"{'Name':<10} {'Mode':<10} {'Score':<5}")
        print("-" * 30)
        for record in self.game_record.records:
            print(f"{record.name:<10} {record.mode:<10} {record.score:<5}")
