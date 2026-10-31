"""
GovInfo Hearing MODS & Transcript Parser
-----------------------------------------
Parses MODS metadata records and raw HTML transcripts for GovInfo hearings.
Replicates logic from scripts/python/lib/mods.py, transcript.py, and speakers.py.
"""

from pathlib import Path
import xml.etree.ElementTree as ET

NS = {"m": "http://www.loc.gov/mods/v3"}
NO_TEXT_MARKER = b"<TEXT NOT AVAILABLE>"

def parse_mods_record(mods_path: Path) -> dict:
    """Parse MODS XML record to extract hearing metadata, rosters, and committees."""
    if not mods_path.exists():
        return {}
        
    tree = ET.parse(mods_path)
    root = tree.getroot()
    
    # Extract package metadata
    title_el = root.find(".//m:titleInfo/m:title", NS)
    title = title_el.text.strip() if title_el is not None and title_el.text else ""
    
    # Extract Committees
    committees = []
    for comm in root.findall(".//m:congCommittee", NS):
        committees.append({
            "authority_id": comm.get("authorityId"),
            "chamber": comm.get("chamber"),
            "name": comm.findtext("m:name", default="", namespaces=NS)
        })
        
    # Extract Members
    members = []
    for member in root.findall(".//m:congMember", NS):
        members.append({
            "bioguide_id": member.get("bioGuideId"),
            "name": member.findtext("m:name", default="", namespaces=NS),
            "role": member.get("role")
        })
        
    # Extract Witnesses
    witnesses = [w.text.strip() for w in root.findall(".//m:witness", NS) if w.text]
    
    return {
        "package_id": mods_path.stem,
        "title": title,
        "committees": committees,
        "members": members,
        "witnesses": witnesses,
        "n_members": len(members),
        "n_committees": len(committees)
    }

def process_hearing_transcript(htm_path: Path) -> dict:
    """Parse HTML transcript into structured turns using the 4-space paragraph rule."""
    if not htm_path.exists():
        return {"has_text": False, "turns": [], "has_marker": False}
        
    content_bytes = htm_path.read_bytes()
    has_marker = NO_TEXT_MARKER in content_bytes
    
    lines = content_bytes.decode("utf-8", errors="ignore").splitlines()
    turns = []
    current_turn = []
    
    for line in lines:
        if line.startswith("    "): # 4-space indent paragraph opening
            cleaned = line.strip()
            if cleaned:
                if current_turn:
                    turns.append(" ".join(current_turn))
                current_turn = [cleaned]
        elif current_turn and line.strip():
            current_turn.append(line.strip())
            
    if current_turn:
        turns.append(" ".join(current_turn))
        
    return {
        "has_text": len(turns) > 0 and not has_marker,
        "has_marker": has_marker,
        "turns_count": len(turns),
        "turns": turns
    }

if __name__ == "__main__":
    print("GovInfo Data Processing Script")
