import enum
from sqlalchemy import String, Text, Table, Column, ForeignKey, Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Etat(enum.Enum):
    EN_COURS = "EN_COURS"
    TERMINEE = "TERMINEE"
    ARCHIVEE = "ARCHIVEE"


users_groups = Table(
    "users_groups",
    db.metadata,
    Column("user_id", ForeignKey('users.id'), primary_key=True),
    Column("groupe_id", ForeignKey('groupes.id'), primary_key=True)
)

class User(db.Model):
    __tablename__= "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    prenom: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password : Mapped[str] = mapped_column(String)

    groups: Mapped[list["Groupe"]] = relationship(secondary=users_groups, back_populates="users")

    taches: Mapped[list["Tache"]] = relationship(back_populates="user")

    listes_taches: Mapped[list["ListeTache"]] = relationship(back_populates="user")


class Groupe(db.Model):
    __tablename__= "groupes"
    id: Mapped[int] = mapped_column(primary_key=True)
    libelle: Mapped[str] = mapped_column(String(100))
    description : Mapped[str] = mapped_column(Text)

    users: Mapped[list["User"]] = relationship(secondary=users_groups, back_populates="groupes")

    listes_taches: Mapped[list["ListeTache"]] = relationship(back_populates="groupe")

class ListeTache(db.Model):
    __tablename__= "liste_taches"
    id: Mapped[int] = mapped_column(primary_key=True)
    libelle: Mapped[str] = mapped_column(String(100))
    description : Mapped[str] = mapped_column(Text)

    taches: Mapped[list["Tache"]] = relationship(back_populates="liste_tache")

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="listes_taches")

    groupe_id: Mapped[int] = mapped_column(ForeignKey('groupes.id'), primary_key=True)
    groupe: Mapped["Groupe"] = relationship(back_populates="listes_taches")


class Tache(db.Model):
    __tablename__= "taches"
    id: Mapped[int] = mapped_column(primary_key=True)
    libelle: Mapped[str] = mapped_column(String(100))
    description : Mapped[str] = mapped_column(Text)
    etat: Mapped[Etat] = mapped_column(Enum(Etat))

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="taches")

    liste_tache_id: Mapped[int] = mapped_column(ForeignKey('liste_taches.id'), primary_key=True)
    liste_tache: Mapped["ListeTache"] = relationship(back_populates="taches")