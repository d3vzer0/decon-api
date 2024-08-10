import requests
import json


class Technique:
    def __init__(self, technique):
        self.technique = technique

    @classmethod
    def from_cti(cls, technique: dict) -> 'Technique':
        """Format technique to match expected API schema

        Args:
            technique (_type_): _description_

        Returns:
            _type_: _description_
        """
        technique = { 
            'id': technique['id'],
            'technique_id': technique['external_references'][0]['external_id'],
            'name':technique['name'],
            'description': technique['description'],
            'platforms': technique['x_mitre_platforms'], 
            'permissions_required': technique.get('x_mitre_permissions_required', []),
            'data_sources': technique.get('x_mitre_data_sources', []),
            'references': technique['external_references'],
            'kill_chain_phases': [phase['phase_name'] for phase in technique['kill_chain_phases']],
            'is_subtechnique': technique.get('x_mitre_is_subtechnique', False),
            'data_sources_available': [],
            'actors': []
        }
        return cls(technique)


class Actor:
    def __init__(self, actor):
        self.actor = actor

    @classmethod
    def from_cti(cls, actor: dict) -> 'Actor':
        """Format actor to match expected API schema

        Args:
            actor (dict): actor dictionary

        Returns:
            Actor: Actor class
        """
        actor = {
            'id': actor['id'], 
            'actor_id': actor['external_references'][0]['external_id'],
            'name': actor['name'],
            'references': actor['external_references'],
            'aliases': actor.get('aliases', None),
            'description': actor.get('description', None),
            'techniques': []
        }
        return cls(actor)


class MitreAttck:
    def __init__(self, actors: list = None, techniques: list = None):
        self.actors = actors
        self.techniques = techniques

    @staticmethod
    def __make_related(actors, techniques: list, relationships):
        actors_by_id = {a.actor['id']: a.actor['actor_id'] for (key, a) in actors.items()}
        t_by_id = {t.technique['id']: t.technique['technique_id'] for (key, t) in techniques.items()}

        for relationship in relationships:
            has_technique = t_by_id.get(relationship['target_ref'], None)
            has_actor = actors_by_id.get(relationship['source_ref'], None)

            if has_actor and has_technique:
                related_technique = techniques[has_technique]
                related_actor = actors[has_actor]
            
                related_technique.technique['actors'].append({
                    'actor_id': related_actor.actor['actor_id'],
                    'name': related_actor.actor['name']
                })

                related_actor.actor['techniques'].append({
                    'technique_id': related_technique.technique['technique_id'],
                    'name': related_technique.technique['name']
                })
            
        return actors, techniques

    @classmethod
    def from_cti(cls, cti_url='https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'):
        """Initialise MitreAttck class from Attck github

        Args:
            cti_url (str, optional): _description_. Defaults to 'https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'.

        Returns:
            _type_: _description_
        """
        # Since github does not return a valid json response header
        # we have to load the response as text first and parse afterwards
        get_entries = requests.get(cti_url)
        get_entries = get_entries.text

        actors, techniques = {}, {}
        relationships = []
        for entry in json.loads(get_entries)['objects']:
            if entry.get('revoked', False) == False:
                if entry['type'] == 'attack-pattern':
                    technique_obj =  Technique.from_cti(entry)
                    techniques[technique_obj.technique['technique_id']] = technique_obj

                elif entry['type'] == 'intrusion-set':
                    actor_obj = Actor.from_cti(entry)
                    actors[actor_obj.actor['actor_id']] = actor_obj

                elif entry['type'] == 'relationship':
                    relationships.append(entry)

        actors, techniques = cls.__make_related(actors, techniques, relationships)
        return cls(actors, techniques)
