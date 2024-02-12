import requests
import json

class Technique:
    def __init__(self, technique):
        self.technique = technique

    @classmethod
    def from_cti(cls, technique):
        ''' Format technique to match expected API schema '''
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
    def from_cti(cls, actor):
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
    def __init__(self, actors = None, techniques = None):
        self.actors = actors
        self.techniques = techniques

    @staticmethod
    def __make_related(actors, techniques, relationships):
        for relationship in relationships:
            related_technique = techniques.get(relationship['target_ref'], None)
            related_actor = actors.get(relationship['source_ref'], None)
            if related_actor and related_technique:
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
        # Since github does not return a valid json response header
        # we have to load the response as text first and parse afterwards
        get_entries = requests.get(cti_url)
        get_entries = get_entries.text

        actors, techniques, relationships = {}, {}, []
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
