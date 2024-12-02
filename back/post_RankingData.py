from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text, Boolean, ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from back.get_DB_Connection import DATABASE_URI

# Database connection setup
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Define the models for both tables
class UserModelRanking(Base):
    __tablename__ = 'user_model_ranking'
    
    submission_id = Column(Integer, primary_key=True, autoincrement=True)
    em_index = Column(Integer, nullable=False)
    vote_name = Column(String, nullable=False)
    chosen_model = Column(Integer, nullable=False)  # 0 for GPT, 1 for RTM
    consent_given = Column(Boolean, nullable=False)
    expertise_level = Column(Integer, nullable=False)
    additional_labels = Column(ARRAY(String))
    timestamp = Column(DateTime, default=datetime.utcnow)

class VoteFrequencySoftmax(Base):
    __tablename__= 'vote_ranking_softmax'
    vote_index = Column(Integer, primary_key=True, nullable=False)  # Matches index in main corpus table
    vote_Name = Column(String, nullable=False)
    appearance_count = Column(Integer, nullable=False)  # Tracks appearances


# Create tables with new schema
Base.metadata.create_all(engine)

# Create a database session
Session = sessionmaker(bind=engine)

def save_UserModelRanking_To_Postgres(data_To_Send: dict):
    """
    Function to save UserModelRanking data and update appearance count in VoteFrequencySoftmax.
    """
    session = Session()
    try:
        # Ensure all integers are cast to native Python int
        data_To_Send['vote_index'] = int(data_To_Send['vote_index'])
        data_To_Send['chosen_model'] = int(data_To_Send['chosen_model'])
        data_To_Send['expertise_level'] = int(data_To_Send['expertise_level'])

        # Insert new entry in the UserModelRanking table
        new_entry = UserModelRanking(
            em_index=data_To_Send['vote_index'],
            vote_name=data_To_Send['vote_name'],
            chosen_model=data_To_Send['chosen_model'],
            consent_given=bool(data_To_Send['consent_given']),
            expertise_level=data_To_Send['expertise_level'],
            additional_labels=data_To_Send.get('additional_labels', []),
            timestamp=datetime.now()
        )
        session.add(new_entry)
        session.commit()  # Commit to generate a submission_id for the new entry

        # Check for existing entry in VoteFrequencySoftmax
        existing_softmax_entry = session.query(VoteFrequencySoftmax).filter_by(vote_index=data_To_Send['vote_index']).first()

        if existing_softmax_entry:
            # Increment appearance_count if entry exists
            existing_softmax_entry.appearance_count += 1
        else:
            # Create a new entry if it doesn't exist
            new_softmax_entry = VoteFrequencySoftmax(
                vote_index=data_To_Send['vote_index'],
                vote_Name=data_To_Send['vote_name'],
                appearance_count=1
            )
            session.add(new_softmax_entry)

        # Commit changes to VoteFrequencySoftmax
        session.commit()

    except Exception as e:
        # Rollback session in case of error
        session.rollback()
        raise e
    finally:
        # Close the session
        session.close()

