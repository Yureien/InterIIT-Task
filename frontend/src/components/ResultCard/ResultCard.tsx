import React from 'react';
import './ResultCard.scss';

import { Result } from '../../data';
import { Image, Card, Col, Row } from 'react-bootstrap';

interface ResultCardProps {
    result: Result;
};

function ResultCard({ result }: ResultCardProps) {
    console.log(result);
    const handleClick = () => {
        console.log(result.description);
        console.log(result.body);
        window.open(result.link, '_blank');
    };

    let description = result.description || result.body;
    if (description && description.length > 400) {
        description = `${description.substring(0, 400)}...`;
    }

    return (
        <Card className="result-card m-4 shadow rounded-lg" onClick={handleClick}>
            <Row className="g-0">
                <Col md={result.image ? 8 : 12}>
                    <Card.Body>
                        <Card.Title>{result.title}</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">{result.link}</Card.Subtitle>
                        <Card.Text>{description}</Card.Text>
                    </Card.Body>
                </Col>
                {result.image && (
                    <Col md={4} className="d-none d-md-block">
                        <Image src={result.image} alt={result.title} fluid className="rounded-end" />
                    </Col>
                )}
            </Row>
        </Card>
    )
};

export default ResultCard;